import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from cuztomisable.db.models.users.user import User
from cuztomisable.dependencies import get_current_user, get_db
from cuztomisable.schemas.roles.permission import RolePermissionCreate, RolePermissionResponse
from cuztomisable.schemas.roles.role import RoleCreate, RoleResponse, RoleUpdate
from cuztomisable.services.roles.permission import RolePermissionService
from cuztomisable.services.roles.role import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RoleResponse])
def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return RoleService(db).get_all()


@router.get("/{role_id}", response_model=RoleResponse)
def show(role_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    role = RoleService(db).get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return role


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def store(data: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return RoleService(db).create(data)


@router.put("/{role_id}", response_model=RoleResponse)
def update(role_id: uuid.UUID, data: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    role = RoleService(db).update(role_id, data)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(role_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    deleted = RoleService(db).delete(role_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{role_id}/permissions", response_model=list[RolePermissionResponse])
def index_permissions(role_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return RolePermissionService(db).get_by_role(role_id)


@router.post("/{role_id}/permissions", response_model=RolePermissionResponse, status_code=status.HTTP_201_CREATED)
def store_permission(role_id: uuid.UUID, data: RolePermissionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return RolePermissionService(db).create(role_id, data)


@router.delete("/{role_id}/permissions/{role_permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_permission(role_id: uuid.UUID, role_permission_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    deleted = RolePermissionService(db).delete(role_permission_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
