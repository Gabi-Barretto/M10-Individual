from fastapi import FastAPI
from app.routes import user_routes
from app.database import engine
from app.models import user_model

app = FastAPI()

user_model.Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
