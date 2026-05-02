from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import Annotated

from database.database import get_session
from app.models import InventoryItem, Order, Owner
from app.schema import InventoryItemCreate, OrderCreate, InventoryItemUpdate


SessionDep = Annotated[Session, Depends(get_session)]


def create_inventory(item: InventoryItemCreate, session: SessionDep, current_owner: Owner):
    inventory = InventoryItem(
        name=item.name,
        description=item.description,
        quantity=item.quantity,
        price=item.price,
        owner_id=current_owner.id
    )

    session.add(inventory)
    session.commit()
    session.refresh(inventory)

    return inventory


def show_inventory(session: SessionDep, current_owner: Owner):
    inventory = session.exec(select(InventoryItem).where(InventoryItem.owner_id == current_owner.id)).all()
    return inventory     


def update_inventory(item_data: InventoryItemUpdate, item_id: int, current_owner: Owner, session: Session):
    item = session.get(InventoryItem, item_id)

    if not item:
        raise HTTPException(404, "Item not found")

    if item.owner_id != current_owner.id:
        raise HTTPException(403, "Not your item")

    update_data = item_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    session.commit()
    session.refresh(item)
    return item 


def delete_inventory(item_id: int, session: SessionDep, current_owner: Owner):
    inventory = session.exec(select(InventoryItem).where(InventoryItem.id == item_id)).first()
    if not inventory:
        raise HTTPException(404, "Item not found")
    if inventory.owner_id != current_owner.id:
        raise HTTPException(403, "You are not authorized to delete this item")
    session.delete(inventory)
    session.commit()
    return {"message": "Item deleted successfully"}

      
def create_order(order_data: OrderCreate, session: SessionDep, current_owner: Owner):
    item = session.get(InventoryItem, order_data.item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    order = Order(
        item_id=order_data.item_id,
        owner_id=current_owner.id,
        quantity=order_data.quantity,
        total_price=order_data.quantity * item.price
    )
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def show_order(session: SessionDep, current_owner: Owner):
    order = session.exec(select(Order).where(Order.owner_id == current_owner.id)).all()
    return order


def update_order(order_data: OrderCreate, order_id: int, current_owner: Owner, session: Session):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    if order.owner_id != current_owner.id:
        raise HTTPException(403, "Not your order")

    item = session.get(InventoryItem, order_data.item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    order.item_id = order_data.item_id
    order.quantity = order_data.quantity
    order.total_price = order_data.quantity * item.price

    session.commit()
    session.refresh(order)
    return order    


def delete_order(order_id: int, session: SessionDep, current_owner: Owner):
    order = session.exec(select(Order).where(Order.id == order_id)).first()
    if not order:
        raise HTTPException(404, "Order not found")
    if order.owner_id != current_owner.id:
        raise HTTPException(403, "You are not authorized to delete this order")
    session.delete(order)
    session.commit()
    return {"message": "Order deleted successfully"}   

