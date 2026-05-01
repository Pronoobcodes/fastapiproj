from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated, List
from sqlmodel import Session

from database.database import get_session
from app.models import Owner 
from app.schema import OwnerCreate, OwnerResponse, OwnerLogin
from app.crud import create_owner, login_owner, get_current_owner, show_owner, update_owner, update_password


SessionDep = Annotated[Session, Depends(get_session)]
OwnerDep = Annotated[Owner, Depends(get_current_owner)]
manger_router = APIRouter(prefix="/manager", tags=["manager"])


@manger_router.post("/create", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
def create_owner_route(owner: OwnerCreate, session: SessionDep):
    return create_owner(owner, session)


@manger_router.post("/login", response_model=OwnerResponse, status_code=status.HTTP_200_OK)
def login_route(owner: OwnerLogin, session: SessionDep):
    return login_owner(owner, session)


@manger_router.get("/{owner_id}", response_model=OwnerResponse, status_code=status.HTTP_200_OK) #, dependencies=[Depends(get_current_owner)]'''
def show_owner_route(owner_id: int, session: SessionDep):
    return show_owner(owner_id, session)


@manger_router.put("/{owner_id}", response_model=OwnerResponse, status_code=status.HTTP_200_OK) #, dependencies=[Depends(get_current_owner)]'''
def update_owner_route(owner_id: int, session: SessionDep):
    return update_owner(owner_id, session)    


@manger_router.put("/{owner_id}", response_model=OwnerResponse, status_code=status.HTTP_200_OK)
def update_password_route(owner_id: int, session: SessionDep):
    return update_password(owner_id, session)    