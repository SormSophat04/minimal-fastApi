from app.core.exceptions import ConflictError, NotFoundError
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, payload: UserCreate):
        if self.repo.get_by_email(str(payload.email)):
            raise ConflictError("Email already exists")
        return self.repo.create(name=payload.name, email=str(payload.email))

    def list_users(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip=skip, limit=limit)

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def delete_user(self, user_id: int) -> int:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        self.repo.delete(user)
        return user_id
