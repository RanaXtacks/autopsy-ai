# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware

# IMPORTANT: You may need to adjust these import paths depending on exactly how Trae named the variables.
# We are assuming you have a database.py file with your SQLAlchemy Base and engine.
try:
    from api.database import engine, Base
    # Import all your models here so SQLAlchemy knows they exist before creating tables
    from api.models_db import User, BehaviorSession, Habit, ProductivityScore
except ImportError as e:
    print(f"Warning: Database configuration not found or models missing: {e}")

# Try importing the routers generated during the sprints
try:
    from api.orchestration import intelligence_layer_v1
    from api.routers import chat_router, upload_router
except ImportError:
    print("Warning: Routers not found. Check your api/ folders.")

app = FastAPI(
    title="Autopsy AI API",
    description="Behavioral Intelligence & Predictive Analytics Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database Tables on Startup
@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Skipping database creation: {e}")

@app.get("/")
async def root():
    return {"status": "online", "message": "Autopsy AI Backend is running."}

# Wire up the endpoints
try:
    # Assuming the routers were named 'router' inside their respective files
    app.include_router(intelligence_layer_v1.router, prefix="/api/v1/intelligence", tags=["Intelligence"])
    app.include_router(chat_router.router, prefix="/api/chat", tags=["AI Investigator"])
    app.include_router(upload_router.router, prefix="/api/v1/data", tags=["Data Upload"])
except NameError:
    pass