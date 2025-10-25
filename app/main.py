from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import engine
from app.models.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="API",
    description="Backend API for a technical blog platform.",
    lifespan=lifespan,
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root API endpoint
    """
    return {"message": "My Blog API!"}
