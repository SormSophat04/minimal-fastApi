from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


def _doc_to_dict(doc: dict) -> dict:
    return {"id": str(doc["_id"]), "title": doc["title"], "content": doc.get("content", "")}


class NoteRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col = db["notes"]

    async def create(self, *, title: str, content: str) -> dict:
        res = await self.col.insert_one({"title": title, "content": content})
        doc = await self.col.find_one({"_id": res.inserted_id})
        return _doc_to_dict(doc)

    async def list(self, skip: int = 0, limit: int = 100) -> list[dict]:
        cursor = self.col.find().skip(skip).limit(limit)
        return [_doc_to_dict(d) async for d in cursor]

    async def get_by_id(self, note_id: str) -> dict | None:
        if not ObjectId.is_valid(note_id):
            return None
        doc = await self.col.find_one({"_id": ObjectId(note_id)})
        return _doc_to_dict(doc) if doc else None

    async def delete(self, note_id: str) -> bool:
        if not ObjectId.is_valid(note_id):
            return False
        res = await self.col.delete_one({"_id": ObjectId(note_id)})
        return res.deleted_count == 1
