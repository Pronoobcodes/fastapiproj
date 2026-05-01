from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import Annotated

from app.schema import InventoryItemResponse, OrderResponse, InventoryItemCreate, OrderCreate
from app.models import Owner
from app.crud.store import create_inventory, show_inventory, update_inventory, delete_inventory, create_order, show_order, update_order, delete_order
from app.crud.users import get_current_owner
from database.database import get_session


SessionDep = Annotated[Session, Depends(get_session)]
OwnerDep = Annotated[Owner, Depends(get_current_owner)]

store_router = APIRouter(prefix="/store", tags=["store"])


@store_router.post("/create", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_route(item: InventoryItemCreate, session: SessionDep, current_owner: OwnerDep):
    return create_inventory(item, session, current_owner)


@store_router.get("/", response_model=list[InventoryItemResponse])
def show_inventory_route(session: SessionDep, current_owner: OwnerDep):
    return show_inventory(session, current_owner)


@store_router.put("/{item_id}", response_model=InventoryItemResponse)
def update_inventory_route(item_id: int, session: SessionDep, current_owner: OwnerDep):
    return update_inventory(item_id, session, current_owner)


@store_router.delete("/{item_id}", response_model=InventoryItemResponse)
def delete_inventory_route(item_id: int, session: SessionDep, current_owner: OwnerDep):
    return delete_inventory(item_id, session, current_owner)


@store_router.post("/order", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_route(order: OrderCreate, session: SessionDep, current_owner: OwnerDep):
    return create_order(order, session, current_owner)


@store_router.get("/order", response_model=list[OrderResponse])
def show_order_route(session: SessionDep, current_owner: OwnerDep):
    return show_order(session, current_owner)


@store_router.put("/order/{order_id}", response_model=OrderResponse)
def update_order_route(order_id: int, session: SessionDep, current_owner: OwnerDep):
    return update_order(order_id, session, current_owner)


@store_router.delete("/order/{order_id}", response_model=OrderResponse)
def delete_order_route(order_id: int, session: SessionDep, current_owner: OwnerDep):
    return delete_order(order_id, session, current_owner)