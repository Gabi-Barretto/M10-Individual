from fastapi import FastAPI
from routes import log_routes
from database import engine
from models import log_model

app = FastAPI()

log_model.Base.metadata.create_all(bind=engine)

app.include_router(log_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
