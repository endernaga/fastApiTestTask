from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from routers.node import node_crud
from routers.schemas import Node

router = APIRouter(
    prefix="/node",
    responses={404: {"description": "Not found"}}
)


@router.post("/{node_id}/add_node", response_model=Node)
def add_new_node(node_id: int, node_data: Node, db: Session = Depends(get_db)):
    node = node_crud.create_node(db, node_data, node_id)
    return node
