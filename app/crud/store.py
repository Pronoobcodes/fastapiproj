from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import Annotated

from database.database import get_session
from app.models import InventoryItem, Order
from app.schema import InventoryItemCreate, InventoryItemResponse, OrderCreate, OrderResponse
from app.security import hash_password, verify_password

