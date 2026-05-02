from sqlmodel import SQLModel, Field
from typing import Optional, List


class InventoryItemCreate(SQLModel):
    name: str
    description: Optional[str] = None
    quantity: int
    price: float


class InventoryItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None


class InventoryItemResponse(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    quantity: int
    price: float
    owner_id: int


class OrderCreate(SQLModel):
    item_id: int
    quantity: int


class OrderResponse(SQLModel):
    id: int
    item_id: int
    owner_id: int
    quantity: int
    total_price: float

    item: Optional[InventoryItemResponse] = None


class OwnerCreate(SQLModel):
    name: str
    email: str
    password: str


class OwnerUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None


class OwnerResponse(SQLModel):  
    id: int
    name: str
    email: str


class OwnerWithDetails(OwnerResponse):
    items: List[InventoryItemResponse] = Field(default_factory=list)
    orders: List[OrderResponse] = Field(default_factory=list)


class OwnerLogin(SQLModel):
    email: str
    password: str


class PasswordUpdate(SQLModel):
    old_password: str
    new_password: str
    confirm_password: str


class Token(SQLModel):
    access_token: str
    token_type: str