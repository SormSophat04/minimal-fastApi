from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.mongo import close_mongo, ping_mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    try:
        await ping_mongo()
    except Exception:
        pass
    yield
    await close_mongo()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    init_db()

    @app.get("/", tags=["root"])
    def root():
        return {"message": "FastAPI + Database connected", "docs": "/docs"}

    app.include_router(v1_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()
