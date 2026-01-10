from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from app.config.database import db
from app.routes import auth# Assuming this is where your auth router is defined
from app.routes import admin
from app.routes import user
app = FastAPI()

# Add CORS middleware to handle OPTIONS preflights and allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev/testing; change to specific origins like ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows Content-Type, Authorization, etc.
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Kogoma Health Solution backend is running 🚑"}