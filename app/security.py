from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jose import jwt

password_hash = PasswordHash.recommended()
SECRET_KEY = "49c7c1f727214f5b53ffa984d13f8429b5441856013875da5acb7bef2ed1dcf6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)