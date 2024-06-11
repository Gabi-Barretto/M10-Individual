from fastapi import Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from . import app, models
import shutil

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename
    with open(f"./uploaded_images/{filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    new_image = models.Image(filename=filename, status="uploaded")
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    
    # Aqui você pode adicionar lógica de processamento de imagem
    new_image.status = "processed"
    db.commit()
    
    return {"filename": filename, "status": new_image.status}
