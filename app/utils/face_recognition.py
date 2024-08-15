from deepface import DeepFace
import os

def verify_face(stored_image_path, uploaded_image_path):
    try:
        result = DeepFace.verify(stored_image_path, uploaded_image_path)
        return result['verified']
    except Exception as e:
        print(f"Error in face verification: {e}")
        return False