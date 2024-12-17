from fastapi import WebSocket, Depends, APIRouter
from app.services.user_service import UserService
from typing import Dict
from app.dependencies.database import get_db
router = APIRouter()

@router.websocket("/register/{token}")
async def websocket_register(websocket: WebSocket, token: str, session = Depends(get_db)):
    user_service = UserService(session)
    try:
        await user_service.register_face_user(websocket, token)
    except Exception as e:
        await websocket.close()
        raise e

@router.websocket("/verify/{token}")
async def websocket_verify(websocket: WebSocket, token: str, session = Depends(get_db)):
    user_service = UserService(session)
    try:
        await user_service.verify_face_user(websocket, token)
    except Exception as e:
        await websocket.close()
        raise e

@router.websocket("/detection_face")
async def websocket_detection_face(websocket: WebSocket, session = Depends(get_db)):
    user_service = UserService(session)
    try:
        await user_service.detection_face(websocket)
    except Exception as e:
        print(e)
        await websocket.close()
        raise e