import time

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundError
from app.db.mongo import get_mongo_client, get_mongo_db
from app.repositories.note import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse
from app.services.note import NoteService

router = APIRouter(prefix="/mongo", tags=["mongo"])


def get_note_service(
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> NoteService:
    return NoteService(NoteRepository(db))


@router.get("/health")
async def mongo_health():
    start = time.perf_counter()
    try:
        await get_mongo_client().admin.command("ping")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"MongoDB unreachable: {e}")
    latency_ms = round((time.perf_counter() - start) * 1000, 2)
    db = get_mongo_db()
    collections = await db.list_collection_names()
    return {
        "status": "ok",
        "database": db.name,
        "latency_ms": latency_ms,
        "collections": collections,
    }


@router.post("/notes", response_model=NoteResponse, status_code=201)
async def create_note(payload: NoteCreate, service: NoteService = Depends(get_note_service)):
    return await service.create_note(payload)


@router.get("/notes", response_model=list[NoteResponse])
async def list_notes(skip: int = 0, limit: int = 100, service: NoteService = Depends(get_note_service)):
    return await service.list_notes(skip=skip, limit=limit)


@router.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str, service: NoteService = Depends(get_note_service)):
    try:
        return await service.get_note(note_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/notes/{note_id}")
async def delete_note(note_id: str, service: NoteService = Depends(get_note_service)):
    try:
        deleted_id = await service.delete_note(note_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"deleted": True, "id": deleted_id}
