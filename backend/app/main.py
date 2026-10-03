from fastapi import FastAPI

from app.routes.user_routes import router as user_router


app = FastAPI(
    title="AI Fitness & Nutrition Assistant",
    description="Multimodal AI fitness and nutrition assistant",
    version="1.0.0",
)


app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "AI Fitness & Nutrition Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }