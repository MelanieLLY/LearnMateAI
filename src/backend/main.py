from fastapi import FastAPI

from src.backend.database import Base, engine
from src.backend.routers.modules import router as modules_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LearnMateAI API", version="0.1.0")
app.include_router(modules_router, prefix="/api/v1")
