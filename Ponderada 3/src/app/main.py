from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database.database import create_db, get_db
from app.controllers.user_controller import router as user_router
from app.controllers.image_controller import router as image_router
from app.controllers.log_controller import router as log_router
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(image_router, prefix="/image", tags=["image"])
app.include_router(log_router, prefix="/logs", tags=["logs"])

@app.on_event("startup")
def startup_event():
    if not os.path.exists("test.db"):
        print("Database does not exist. Creating database...")
        create_db()
        print("Database created successfully.")
    else:
        print("Database already exists.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
