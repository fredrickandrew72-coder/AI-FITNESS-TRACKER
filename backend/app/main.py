from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user_routes import router as user_router
from app.routes.food_log_routes import router as food_log_router
from app.routes.nutrition_routes import router as nutrition_router
from app.routes.food_routes import router as food_router
from app.routes.food_detection_routes import router as food_detection_router
from app.routes.recipe_nutrition_routes import router as recipe_nutrition_router

app = FastAPI(
    title="AI Fitness & Nutrition Assistant",
    description="Multimodal AI fitness and nutrition assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(food_log_router)
app.include_router(nutrition_router)
app.include_router(food_router)
app.include_router(food_detection_router)
app.include_router(recipe_nutrition_router)


@app.get("/")
def root():
    return {"message": "AI Fitness & Nutrition Assistant API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
