from sqlalchemy.orm import Session

from database import models
from dependencies import get_db
from routers.schemas import WorkFlow, StartNode


def create_workflow(db: Session, workflow: WorkFlow):
    db_workflow = models.WorkFlow()

    if workflow.start_node:  # its give ability to create start node with workflow
        db_start_node = models.Node(**workflow.start_node.dict())
        db_workflow.start_node = db_start_node
        db.add(db_start_node)
        db.commit()
        db.refresh(db_start_node)

    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)


def get_workflow(db: Session, workflow_id: int):
    return db.query(models.WorkFlow).filter(models.WorkFlow.id == workflow_id).first()


def delete_workflow(db: Session, workflow_id: int):
    workflow = get_workflow(db, workflow_id)
    if not workflow:
        raise ValueError(f"Workflow with id {workflow_id} not exist")
    db.delete(workflow)
    db.commit()


def update_workflow(db: Session, workflow_id: int, start_node: StartNode):
    workflow = get_workflow(db, workflow_id)
    db_start_node = models.Node(**start_node.dict())
    workflow.start_node = db_start_node
    db.add(db_start_node)
    db.commit()
    db.refresh(db_start_node)


if __name__ == "__main__":
    db = next(get_db())
    update_workflow(db, 1, StartNode())
