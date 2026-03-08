from fastapi import FastAPI
from api.routes import health_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="API PDF Reader",
        description="PDF Reader API with AI capabilities",
        version="0.1.0"
    )
    
    # Include the health router
    app.include_router(health_router, prefix="/api", tags=["Health"])
    
    return app
