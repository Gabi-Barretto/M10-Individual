from fastapi import FastAPI
from routes import user_routes
from database import engine
from models import user_model

app = FastAPI()

user_model.Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
