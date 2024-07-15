from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from routers.workflow import workflow_crud
from dependencies import get_db
from routers.schemas import WorkFlow, WorkFlowDisplay

router = APIRouter(
    prefix="/workflow",
    responses={404: {"description": "Not found"}}
)


@router.post("/workflow", response_model=WorkFlowDisplay)
async def create_workflow(workflow: WorkFlow, db: Session = Depends(get_db)):
    if workflow is None:
        raise HTTPException(status_code=400, detail="Invalid workflow data")
    created_workflow = workflow_crud.create_workflow(db, workflow)
    return created_workflow


@router.get("/workflow/{workflow_id}", response_model=WorkFlowDisplay)
async def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = workflow_crud.get_workflow(db, workflow_id)
    return workflow


@router.put("/workflow/{workflow_id}", response_model=None)
async def update_workflow(workflow_id: int, start_node: Annotated[int, Body()] = None, db: Session = Depends(get_db)) -> WorkFlow:
    if not start_node:
        raise HTTPException(status_code=400, detail="start_node is required")
    workflow = workflow_crud.update_workflow(db, workflow_id, start_node)
    return workflow


@router.delete("/workflow/{workflow_id}")
async def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    return workflow_crud.delete_workflow(db, workflow_id)
