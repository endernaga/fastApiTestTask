from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette import status

from dependencies import get_db
from routers.deserializer import serializer_from_db_to_schema
from routers.node import node_crud
from routers.schemas import CreateNodeSchema, DisplayNodeSchema

router = APIRouter(
    prefix="/node",
    responses={404: {"description": "Not found"}}
)


@router.post("/{node_id}/add_node", response_model=DisplayNodeSchema)
def add_new_node(node_id: int, node_data: CreateNodeSchema, db: Session = Depends(get_db)):
    node = node_crud.create_node(db, node_data, node_id)
    return serializer_from_db_to_schema(node)


@router.get("/{node_id}/", response_model=DisplayNodeSchema)
def get_node(node_id: int, db: Session = Depends(get_db)):
    return serializer_from_db_to_schema(node_crud.get_node(db, node_id))


@router.delete("/{node_id}")
def delete_node(node_id: int, db: Session = Depends(get_db)):
    node_crud.delete_node(db, node_id)
    return JSONResponse(content={"status": "success"}, status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{node_id}")
def update_node(node_id: int, node_data: CreateNodeSchema, db: Session = Depends(get_db)):
    node = node_crud.update_node(db, node_id, node_data)
    return serializer_from_db_to_schema(node)
