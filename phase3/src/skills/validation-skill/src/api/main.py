from fastapi import FastAPI
from .routes.validation_routes import router as validation_router

# Create FastAPI app instance
app = FastAPI(
    title="Validation Service",
    description="Service for validating content for safety and correctness",
    version="1.0.0"
)

# Include API routes
app.include_router(validation_router, prefix="/api/v1", tags=["validation"])

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "validation-skill"}