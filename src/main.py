from fastapi import FastAPI
from src.api.routes import health_router, documents_router

app = FastAPI(
    title="API PDF Reader",
    description="PDF Reader API with AI capabilities",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(documents_router, prefix="/api/documents", tags=["Documents"])


@app.get("/")
async def root():
    return {"message": "PDF Reader API", "status": "running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
