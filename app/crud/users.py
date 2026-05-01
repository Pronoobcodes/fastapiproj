from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import Annotated
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from database.database import get_session
from app.models import Owner
from app.schema import OwnerCreate, OwnerUpdate, OwnerLogin, PasswordUpdate 
from app.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

SessionDep = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/manager/login")


def create_owner(owner_data: OwnerCreate, session: SessionDep):
    existing = session.exec(
        select(Owner).where(Owner.email == owner_data.email)
    ).first()

    if existing:
        raise HTTPException(400, "Email already registered")

    owner = Owner(
        name=owner_data.name,
        email=owner_data.email.lower().strip(),
        password=hash_password(owner_data.password)
    )

    session.add(owner)
    session.commit()
    session.refresh(owner)
    return owner


def login_owner(owner_login: OwnerLogin, session: SessionDep):
    owner = session.exec(
        select(Owner).where(Owner.email == owner_login.email)
    ).first()

    if not owner or not verify_password(owner_login.password, owner.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": str(owner.id)})
    return {"access_token": token, "token_type": "bearer"}
    

def get_current_owner(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(401, "Invalid credentials")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        owner_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    owner = session.exec(select(Owner).where(Owner.id == owner_id)).first()

    if not owner:
        raise credentials_exception

    return owner


def show_owner(current_owner: Owner, session: SessionDep):
    owner = session.exec(select(Owner).where(Owner.id == current_owner.id).options(selectinload(Owner.items), selectinload(Owner.orders))).first()
    return owner


def update_owner(owner_data: OwnerUpdate, current_owner: Owner, session: SessionDep):
    current_owner.name = owner_data.name
    current_owner.email = owner_data.email

    session.commit()
    session.refresh(current_owner)

    return current_owner   


def update_password(data: PasswordUpdate, current_owner: Owner, session: SessionDep):

    if not verify_password(data.old_password, current_owner.password):
        raise HTTPException(400, "Old password is incorrect")

    if data.new_password != data.confirm_password:
        raise HTTPException(400, "Passwords do not match")

    current_owner.password = hash_password(data.new_password)

    session.commit()

    return {"message": "Password updated successfully"}