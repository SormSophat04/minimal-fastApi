from app.core.exceptions import NotFoundError
from app.repositories.note import NoteRepository
from app.schemas.note import NoteCreate


class NoteService:
    def __init__(self, repo: NoteRepository):
        self.repo = repo

    async def create_note(self, payload: NoteCreate) -> dict:
        return await self.repo.create(title=payload.title, content=payload.content)

    async def list_notes(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return await self.repo.list(skip=skip, limit=limit)

    async def get_note(self, note_id: str) -> dict:
        doc = await self.repo.get_by_id(note_id)
        if not doc:
            raise NotFoundError("Note not found")
        return doc

    async def delete_note(self, note_id: str) -> str:
        ok = await self.repo.delete(note_id)
        if not ok:
            raise NotFoundError("Note not found")
        return note_id
