from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import engine, Base
from app.routes.users import router as users_router
from utils.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(users_router)


@app.get("/")
async def root():
    return {
        "message": "SaaS API is running",
        "docs": "/docs"
    }