from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database.db import SessionLocal, User
from ..utils.face_recognition import verify_face
import shutil
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_user/")
async def create_user(
    db: Session = Depends(get_db),
    full_name: str = Form(...),
    bank_account_name: str = Form(...),
    bank_account_number: str = Form(...),
    email: str = Form(...),
    institution: str = Form(...),
    registration_number: str = Form(...),
    last_yos: str = Form(...),
    photo: UploadFile = File(...)
):
    user = User(
        full_name=full_name,
        bank_account_name=bank_account_name,
        bank_account_number=bank_account_number,
        email=email,
        institution=institution,
        registration_number=registration_number,
        last_yos=last_yos
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)

    os.makedirs("user_photos", exist_ok=True)

    photo_path = f"user_photos/{user.id}_{photo.filename}"
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    user.photo_path = photo_path
    db.commit()

    return {"message": "User created successfully", "user_id": user.id}

@router.post("/verify_user/")
async def verify_user(
    db: Session = Depends(get_db),
    full_name: str = Form(...),
    bank_account_name: str = Form(...),
    bank_account_number: str = Form(...),
    email: str = Form(...),
    institution: str = Form(...),
    registration_number: str = Form(...),
    last_yos: str = Form(...),
    photo: UploadFile = File(...)
):
    user = db.query(User).filter(
        func.lower(User.full_name) == func.lower(full_name),
        func.lower(User.bank_account_name) == func.lower(bank_account_name),
        User.bank_account_number == bank_account_number,
        func.lower(User.email) == func.lower(email),
        func.lower(User.institution) == func.lower(institution),
        User.registration_number == registration_number,
        User.last_yos == last_yos
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found or information doesn't match")

    temp_dir = "temp_photos"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, f"temp_{photo.filename}")

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        
        is_face_match = verify_face(user.photo_path, temp_path)
        
        if is_face_match:
            return {"message": "User verified successfully", "user_id": user.id}
        else:
            raise HTTPException(status_code=401, detail="Face verification failed")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)