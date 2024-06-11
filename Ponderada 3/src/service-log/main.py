from fastapi import FastAPI
from app.routes import log_routes
from app.database import engine
from app.models import log_model

app = FastAPI()

log_model.Base.metadata.create_all(bind=engine)

app.include_router(log_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
