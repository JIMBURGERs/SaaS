from fastapi import FastAPI
from app.routers.users import router as users_router
from utils.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "SaaS API is running", "docs": "/docs"}