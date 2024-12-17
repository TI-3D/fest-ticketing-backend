# app/core/face_recognition.py
import numpy as np
import cv2
import mediapipe as mp
from keras_facenet import FaceNet
import base64
import json

embedder = FaceNet()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def calculate_embedding(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    embedding = embedder.embeddings([rgb_frame])
    return embedding[0]

def check_blink(landmarks):
    left_eye = landmarks.landmark[159].y - landmarks.landmark[145].y
    right_eye = landmarks.landmark[386].y - landmarks.landmark[374].y
    return left_eye < 0.02 and right_eye < 0.02

def check_turn_left(landmarks):
    nose_tip = landmarks.landmark[4].x
    right_face = landmarks.landmark[454].x
    return nose_tip > right_face

def check_turn_right(landmarks):
    nose_tip = landmarks.landmark[4].x
    left_face = landmarks.landmark[234].x
    return nose_tip < left_face

def check_look_straight(landmarks):
    nose_tip = landmarks.landmark[4]
    left_face = landmarks.landmark[234]
    right_face = landmarks.landmark[454]
    face_width = abs(right_face.x - left_face.x)
    nose_position = (nose_tip.x - left_face.x) / face_width
    return 0.45 < nose_position < 0.55
