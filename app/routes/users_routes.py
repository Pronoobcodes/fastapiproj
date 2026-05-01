from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from database.database import get_session
from app.models import Owner
from app.schema import OwnerCreate, OwnerUpdate, OwnerResponse, OwnerWithDetails, OwnerLogin, Token, PasswordUpdate
from app.crud import create_owner, login_owner, get_current_owner, show_owner, update_owner, update_password

SessionDep = Annotated[Session, Depends(get_session)]
OwnerDep = Annotated[Owner, Depends(get_current_owner)]

manger_router = APIRouter(prefix="/manager", tags=["manager"])


@manger_router.post("/create", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
def create_owner_route(owner: OwnerCreate, session: SessionDep):
    return create_owner(owner, session)


@manger_router.post("/login", response_model=Token)
def login_route(session: SessionDep, form: OAuth2PasswordRequestForm = Depends()):
    owner_login = OwnerLogin(email=form.username, password=form.password)
    return login_owner(owner_login, session)


@manger_router.get("/me", response_model=OwnerWithDetails, status_code=status.HTTP_200_OK)
def show_owner_route(current_owner: OwnerDep, session: SessionDep):
    return show_owner(current_owner, session)


@manger_router.put("/me", response_model=OwnerResponse, status_code=status.HTTP_200_OK)
def update_owner_route(owner_data: OwnerUpdate, current_owner: OwnerDep, session: SessionDep):
    return update_owner(owner_data, current_owner, session)


@manger_router.put("/me/password", status_code=status.HTTP_200_OK)
def update_password_route(data: PasswordUpdate, current_owner: OwnerDep, session: SessionDep):
    return update_password(data, current_owner, session)