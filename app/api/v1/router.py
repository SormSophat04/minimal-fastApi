from fastapi import APIRouter

from app.api.v1.endpoints import health, mongo, users

router = APIRouter()
router.include_router(health.router)
router.include_router(users.router)
router.include_router(mongo.router)
