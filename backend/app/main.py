from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.database.database import init_db

# Import API v1 routers
from app.api.v1.auth import router as auth_router
from app.api.v1.profile import router as profile_router
from app.api.v1.careers import router as careers_router
from app.api.v1.assessments import router as assessments_router
from app.api.v1.skills import router as skills_router
from app.api.v1.market import router as market_router
from app.api.v1.roadmaps import router as roadmaps_router
from app.api.v1.learning import router as learning_router
from app.api.v1.projects import router as projects_router
from app.api.v1.challenges import router as challenges_router
from app.api.v1.rewards import router as rewards_router
from app.api.v1.interviews import router as interviews_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.what_if import router as what_if_router
from app.api.v1.sprint import router as sprint_router
from app.api.v1.hackathons import router as hackathons_router
from app.api.v1.dashboard import router as dashboard_router

# Initialize database tables on startup
init_db()

app = FastAPI(
    title=settings.APP_NAME,
    description="SkillForage AI — From Zero to Interview-Ready. Evidence-based student career preparation platform.",
    version="3.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
origins = settings.cors_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Consistent Error Handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err.get("loc", []))
        errors.append(f"{field}: {err.get('msg', 'Invalid input')}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error_type": "ValidationError",
            "message": "Input validation failed.",
            "details": errors
        }
    )

# Root & Health Endpoints
@app.get("/")
def root():
    return {
        "success": True,
        "name": settings.APP_NAME,
        "slogan": "From Zero to Interview-Ready",
        "version": "3.1.0",
        "docs_url": "/docs",
        "api_prefix": "/api/v1"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "database": "connected"
    }

# Include API v1 Routers
api_v1_routers = [
    auth_router,
    profile_router,
    careers_router,
    assessments_router,
    skills_router,
    market_router,
    roadmaps_router,
    learning_router,
    projects_router,
    challenges_router,
    rewards_router,
    interviews_router,
    resumes_router,
    what_if_router,
    sprint_router,
    hackathons_router,
    dashboard_router,
]

for r in api_v1_routers:
    app.include_router(r, prefix="/api/v1")

# Also include auth router at /auth for backward compatibility
app.include_router(auth_router)
