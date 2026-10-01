from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import ConflictError, NotFoundError
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(payload)
    except ConflictError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, service: UserService = Depends(get_user_service)):
    return service.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        return service.get_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        deleted_id = service.delete_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"deleted": True, "id": deleted_id}
