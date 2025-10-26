from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.models.models import Base
from app.routes import post_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    


app = FastAPI(
    title="API",
    description="Backend API for a technical blog platform.",
    lifespan=lifespan,
)

app.include_router(post_routes.router, prefix="/posts", tags=["Posts"])


@app.get("/", tags=["Root"])
async def root():
    """
    Root API endpoint
    """
    return {"message": "My Blog API!"}
