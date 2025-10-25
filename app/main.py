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


app = FastAPI(title="My Blog API", lifespan=lifespan)
