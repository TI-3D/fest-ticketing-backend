import numpy as np
import base64
import json
import time
import cv2
from app.repositories.user_repository import UserRepository
from app.core.face_recognition import calculate_embedding, check_blink, check_turn_left, check_turn_right, check_look_straight, face_mesh
from fastapi import WebSocket
from app.core.security import verify_jwt_token
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import EditUserProfile
from typing import Dict
from fastapi import HTTPException
from app.services.cloudinary_service import CloudinaryService
from app.schemas.response import ResponseSuccess

ACTIONS = ["look_straight", "blink", "turn_left", "turn_right", "look_straight"]
ACTION_MESSAGES = {
    "look_straight": "Please look straight at the camera",
    "blink": "Please blink your eyes",
    "turn_left": "Please turn your head left",
    "turn_right": "Please turn your head right",
}

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)
        self.cloudinary_service = CloudinaryService()
        self.verfication_thresshold = 0.7

    async def register_face_user(self, websocket: WebSocket, token: str):
        await websocket.accept()
        
        # Cari user berdasarkan token
        current_user = verify_jwt_token(token)
        if not current_user:
            await websocket.send_json({
                "status": "error",
                "message": "Invalid token"
            })
            await websocket.close()
            return
        
        user_id = current_user.get("sub")
            
        current_action_index = 0
        start_time = time.time()
        embeddings = []

        # Kirim action pertama
        await websocket.send_json({
            "status": "action_required",
            "action": ACTIONS[0],
            "message": ACTION_MESSAGES[ACTIONS[0]],
            "progress": 0
        })

        try:
            while current_action_index < len(ACTIONS) and time.time() - start_time <= 40:
                current_action = ACTIONS[current_action_index]

                data = await websocket.receive_text()
                frame_data = json.loads(data)
                img_bytes = base64.b64decode(frame_data['image'].split(',')[1])
                nparr = np.frombuffer(img_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Proses face landmarks
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_frame)

                if not results.multi_face_landmarks:
                    await websocket.send_json({
                        "status": "no_face_detected",
                        "action": current_action,
                        "message": "No face detected, please position your face in the frame",
                        "progress": current_action_index * 20
                    })
                    continue

                landmarks = results.multi_face_landmarks[0]
                embedding = calculate_embedding(frame)

                action_completed = False
                if current_action == "blink" and check_blink(landmarks):
                    action_completed = True
                elif current_action == "turn_left" and check_turn_left(landmarks):
                    action_completed = True
                elif current_action == "turn_right" and check_turn_right(landmarks):
                    action_completed = True
                elif current_action == "look_straight" and check_look_straight(landmarks):
                    action_completed = True

                if action_completed:
                    embeddings.append(embedding)
                    current_action_index += 1

                    if current_action_index < len(ACTIONS):
                        await websocket.send_json({
                            "status": "action_completed",
                            "action": ACTIONS[current_action_index],
                            "message": ACTION_MESSAGES[ACTIONS[current_action_index]],
                            "progress": current_action_index * 20
                        })
                    else:
                        mean_embedding = np.mean(embeddings, axis=0).tolist()
                        # Save or update the user's embedding in the database
                        await self.user_repository.save_or_update_embedding(user_id, mean_embedding)

                        await websocket.send_json({
                            "status": "registration_completed",
                            "message": "Registration successfully completed",
                            "progress": 100
                        })
                else:
                    await websocket.send_json({
                        "status": "action_required",
                        "action": current_action,
                        "message": ACTION_MESSAGES[current_action],
                        "progress": current_action_index * 20
                    })

        except Exception as e:
            print(f"Error during registration: {e}")
            await websocket.send_json({
                "status": "error",
                "message": str(e)
            })
        finally:
            await websocket.close()
            
    async def verify_face_user(self, websocket: WebSocket, token: str):
        
        await websocket.accept()        
        
        # Cari user berdasarkan token
        current_user = verify_jwt_token(token)
        if not current_user:
            await websocket.send_json({
                "status": "error",
                "message": "Invalid token"
            })
            await websocket.close()
            return
        
        user_id = current_user.get("sub")
        
        stored_embedding = await self.user_repository.get_embedding_by_user_id(user_id) 
        
        if not stored_embedding:
            await websocket.send_json({
                "status": "error",
                "message": "User not found"
            })
            await websocket.close()
            return
        
        stored_embedding = np.array(json.loads(str(stored_embedding)))
        
        verification_start_time = time.time()
        attempt_count = 0
        max_attempts = 10
        
        try:
            while attempt_count < max_attempts and time.time() - verification_start_time <= 40:
                data = await websocket.receive_text()
                frame_data = json.loads(data)
                img_bytes = base64.b64decode(frame_data['image'].split(',')[1])
                nparr = np.frombuffer(img_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                # Proses gambar dan ekstrak embedding
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_frame)
                
                if not results.multi_face_landmarks:
                    attempt_count += 1
                    await websocket.send_json({
                        "status": "no_face_detected",
                        "message": "No face detected, please position your face in the frame",
                        "attempts_left": max_attempts - attempt_count
                    })
                    continue
                
                current_embedding = calculate_embedding(frame)
                current_embedding = np.array(current_embedding).reshape(1, -1)
                stored_embedding_reshaped = stored_embedding.reshape(1, -1)
                
                # Menghitung similarity score
                similarity_score = cosine_similarity(current_embedding, stored_embedding_reshaped)[0][0]
                print(f"Similarity Score: {similarity_score}")
                
                if similarity_score > self.verfication_thresshold:
                    await websocket.send_json({
                        "status": "verification_successful",
                        "message": "Verification successful",
                        "confidence": float(similarity_score),
                        "progress": 100
                    })
                    break
                else:
                    # attempt_count += 1
                    await websocket.send_json({
                        "status": "verification_failed",
                        "message": f"Processing verification... ",
                        "confidence": float(similarity_score),
                        "progress": (attempt_count * 20)
                    })
                
        except Exception as e:
            print(f"Error during verification: {e}")
            await websocket.send_json({
                "status": "error",
                "message": str(e)
            })
        finally:
            await websocket.close()
    
    async def detection_face(self, websocket: WebSocket):
        await websocket.accept()
        
        attempt_count = 0
        max_attempts = 6
        
        try:
            while True:
                data = await websocket.receive_text()
                frame_data = json.loads(data)
                
                img_bytes = base64.b64decode(frame_data['image'].split(',')[1])
                nparr = np.frombuffer(img_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                # Proses gambar dan ekstrak embedding
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_frame)
                
                if not results.multi_face_landmarks:
                    attempt_count += 1
                    await websocket.send_json({
                        "status": "no_face_detected",
                        "message": f"No face detected. Attempts left: {max_attempts - attempt_count}",
                        "attempts_left": max_attempts - attempt_count
                    })
                    continue
                
                current_embedding = calculate_embedding(frame)
                current_embedding = np.array(current_embedding).reshape(1, -1)
                # Ambil semua data user embedding dari database
                users_data = await self.user_repository.get_all_embeddings()
                user_found = False
                print("Total users: ", len(users_data))
                
                for user_data in users_data:
                    stored_embedding = np.array(json.loads(str(user_data.embedding))).reshape(1, -1)
                    
                    # Hitung kesamaan dengan embedding yang ada
                    similarity_score = cosine_similarity(current_embedding, stored_embedding)[0][0]
                    print(similarity_score)
                    if similarity_score > self.verfication_thresshold:
                        user_found = True
                        await websocket.send_json({
                            "status": "user_found",
                            "message": f"User {user_data.full_name} detected",
                            "confidence": float(similarity_score),
                            "attempts_left": max_attempts - attempt_count
                        })
                        break
                
                if not user_found:
                    # attempt_count += 1
                    await websocket.send_json({
                        "status": "user_not_found",
                        "message": "No matching user found. Please try again.",
                    })
                
                if attempt_count >= max_attempts:
                    await websocket.send_json({
                        "status": "unknown_user",
                        "message": "User not recognized after 3 attempts.",
                        # "attempts_left": 0
                    })
                    attempt_count = 0
                    # break
                
        except Exception as e:
            print(f"Error during detection: {e}")
            await websocket.send_json({
                "status": "error",
                "message": str(e)
            })
        finally:
            await websocket.close()
            
    async def update_user(self, data: EditUserProfile, current: Dict):
        # Fetch current user using the sub from JWT token
        user = await self.user_repository.get_user_by_id(current.get("sub"))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Serialize data and exclude unset and None values
        updated_data = data.model_dump(exclude_unset=True, exclude_none=True)

        # Check for profile picture in the updated data
        if "profile_picture" in updated_data:
            # Upload new profile picture to Cloudinary
            profile_picture_url = self.cloudinary_service.upload_image(
                data.profile_picture.file.read(), folder_name="profiles"
            )
            # If user has an existing profile picture, delete it from Cloudinary
            if user.profile_picture:
                self.cloudinary_service.delete_image_by_url(
                    user.profile_picture, folder_name="profiles"
                )
            # Update profile picture URL in the updated data
            updated_data["profile_picture"] = profile_picture_url["secure_url"]

        # Update user in the repository
        print(updated_data)
        updated_user = await self.user_repository.update(current.get("sub"), updated_data)
        await self.session.commit()
        # Fetch the updated user data from the database after update
        await self.session.refresh(updated_user)

        # Return the response with updated user data
        return ResponseSuccess(message="User updated successfully", data=updated_user)
        