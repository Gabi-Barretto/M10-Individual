from fastapi import FastAPI
from routes import todo_routes
from database import engine
from models import todo_model

app = FastAPI()

todo_model.Base.metadata.create_all(bind=engine)

app.include_router(todo_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
