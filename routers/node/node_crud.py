from sqlalchemy.orm import Session
from typing import Type

from database import models
from dependencies import get_db
from routers.schemas import Node, StartNode, MessageNode, ConditionNode, EndNode


def get_node(db: Session, node_id: int):
    return db.query(models.Node).filter(models.Node.id == node_id).first()


def create_node(db: Session, node: Node, prev_node: Type[int | None] = None):
    if prev_node and node.type == "start":
        raise TypeError("couldn't connect start node to other node. Start node cant have incoming node")
    if prev_node:
        prev_node = get_node(db, prev_node)
        if prev_node.original:
            raise ValueError(f"Node with id {prev_node.id} already have original node")

        if node.type == "condition":
            db_node = models.Node(type=node.type, condition=node.condition)
            db.add(db_node)

            yesNode = create_node(db, node=node.yesNode)
            noNode = create_node(db, node=node.noNode)
            db_node.yesNode = yesNode
            db_node.noNode = noNode

            db.add(db_node)
            db.commit()
            db.refresh(db_node)
            return db_node

        db_node = models.Node(**node.dict())
        prev_node.original = db_node

        db.commit()
        db.refresh(db_node)
        return db_node

    db_node = models.Node(**node.dict())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node


def delete_node(db: Session, node_id: int): # it's function do full delete from selected node
    node = get_node(db, node_id)
    if node.type == "condition":
        delete_node(db, node.yesNode.id)
        delete_node(db, node.noNode.id)

    if node.original:
        delete_node(db, node.original.id)
    db.delete(node)
    db.commit()

    return {"status": "success"}


if __name__ == "__main__":
    db = next(get_db())

    start_node = StartNode()
    message_node = MessageNode(message="Hello World", status="opened")
    condition_node = ConditionNode(yesNode=message_node, noNode=message_node, condition="prev node status = opened")
    end_node = EndNode()

    delete_node(db, 33)
