from pydantic.v1 import Field
from sqlmodel import SQLModel
from typing import List


class InventoryItemCreate(SQLModel):
    name: str
    description: Optional[str] = None
    quantity: int
    price: float


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


class OrderWithItem(OrderResponse):
    item: Optional[InventoryItemResponse]    


class OwnerCreate(SQLModel):
    name: str
    email: str
    password: str


class OwnerResponse(OwnerCreate):
    id: int
    name: str
    email: str


class OwnerWithDetails(OwnerResponse):
    # items: List["InventoryItemResponse"] = []
    # orders: List["OrderResponse"] = []
    items: Optional[List[InventoryItemResponse]] = Field(default_factory=list)
    orders: Optional[List[OrderResponse]] = Field(default_factory=list)
    # items: List[InventoryItemResponse] = Field(default_factory=list)
    # orders: List[OrderResponse] = Field(default_factory=list)


class OwnerLogin(SQLModel):
    email: str
    password: str


class PasswordUpdate(SQLModel):
    old_password: str
    new_password: str
    confirm_password: str    


class token(SQLModel):
    access_token: str
    token_type: str