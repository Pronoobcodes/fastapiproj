from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated

from database.database import get_session
from app.models import Owner
from app.schema import OwnerCreate, OwnerResponse, OwnerLogin
from app.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM


SessionDep = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_owner(owner_data: OwnerCreate, session: Session) -> Owner:
    db_owner = Owner(
        name=owner_data.name,
        email=owner_data.email,
        password=hash_password(owner_data.password)
    )
    session.add(db_owner)
    session.commit()
    session.refresh(db_owner)
    return db_owner


def login_owner(owner_login: OwnerLogin, session: Session):
    owner = session.exec(
        select(Owner).where(Owner.email == owner_login.email)
    ).first()

    if not owner or not verify_password(owner_login.password, owner.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": owner.email})

    return {"access_token": token, "token_type": "bearer"}
    

def get_current_owner(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    owner = session.exec(select(Owner).where(Owner.email == email)).first()
    if owner is None:
        raise credentials_exception
    return owner


def show_owner(current_owner: Owner, session: SessionDep) -> OwnerResponse:
    owner = session.exec(select(Owner).where(Owner.id == current_owner.id).options(selectinload(Owner.items),selectinload(Owner.orders))).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    if owner.id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this owner")
    return owner


def update_owner(owner_data: OwnerCreate, current_owner: Owner, session: SessionDep) -> OwnerResponse:
    owner = session.exec(select(Owner).where(Owner.id == current_owner.id).options(selectinload(Owner.items),selectinload(Owner.orders))).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    if owner.id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this owner")
    current_owner.name = owner_data.name
    current_owner.email = owner_data.email

    session.commit()
    session.refresh(current_owner)
    return current_owner    


def update_password(password: str, current_owner: Owner, session: SessionDep) -> OwnerResponse:
    owner = session.exec(select(Owner).where(Owner.id == current_owner.id).options(selectinload(Owner.items),selectinload(Owner.orders))).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    if owner.id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this owner")
    
    current_owner.password = hash_password(password)

    session.commit()
    session.refresh(current_owner)
    return {"message": "Password updated successfully"}    


