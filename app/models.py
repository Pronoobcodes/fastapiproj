from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class InventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    quantity: int
    price: float

    owner_id: int = Field(foreign_key="owner.id")

    owner: "Owner" = Relationship(back_populates="items")
    orders: List["Order"] = Relationship(back_populates="item")
    

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    item_id: int = Field(foreign_key="inventoryitem.id")
    owner_id: int = Field(foreign_key="owner.id")

    quantity: int
    total_price: float

    item: "InventoryItem" = Relationship(back_populates="orders")
    owner: "Owner" = Relationship(back_populates="orders")


class Owner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str

    items: List["InventoryItem"] = Relationship(back_populates="owner")
    orders: List["Order"] = Relationship(back_populates="owner")