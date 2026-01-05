"""
AEGIS Backend - FastAPI Application
Agentic AI Compliance Platform for Financial Services
"""
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import dashboard, alerts, entities, chat, demo, regulations, jurisdiction

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle events"""
    print("[AEGIS] Backend starting...")
    print("[AEGIS] Dashboard API: /api/dashboard")
    print("[AEGIS] Alerts API: /api/alerts")
    print("[AEGIS] Entities API: /api/entities")
    print("[AEGIS] Chat API: /api/chat")
    print("[AEGIS] Regulations API: /api/regulations")  # Agent 1
    yield
    print("[AEGIS] Backend shutting down...")


# Create FastAPI app
app = FastAPI(
    title="AEGIS API",
    description="Autonomous Enterprise Governance & Intelligence System",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
        "https://aegis-frontend.vercel.app",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(dashboard.router)
app.include_router(alerts.router)
app.include_router(entities.router)
app.include_router(chat.router)
app.include_router(demo.router)
app.include_router(jurisdiction.router)
app.include_router(regulations.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AEGIS API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check for deployment monitoring"""
    return {
        "status": "healthy",
        "agents": {
            "total": 5,
            "online": 5,
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
