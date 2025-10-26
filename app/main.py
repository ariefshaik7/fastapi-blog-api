from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import post_routes, user_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    


app = FastAPI(
    title="API",
    description="Backend API for a technical blog platform.",
    lifespan=lifespan,
)

app.include_router(post_routes.router, prefix="/posts", tags=["Posts"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])


@app.get("/", tags=["Root"])
async def root():
    """
    Root API endpoint
    """
    return {"message": "My Blog API!"}
