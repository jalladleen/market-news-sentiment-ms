from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.routes.news_routes import router as news_router
from src.app.utils.registry_helpers import authenticate, register_service, deregister_service

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; replace with a specific URL in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all headers.
)

# Include routes
app.include_router(news_router, prefix="/api", tags=["News"])

# Register the service with the service registry during startup
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    authenticate()
    register_service()

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    deregister_service()
