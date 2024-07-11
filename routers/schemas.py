import abc
from typing import Literal, List

from pydantic import BaseModel


class Node(BaseModel, abc.ABC):
    type: str
    pass


class StartNode(Node):
    original: Node | None = None
    type: str = "start"

    class Config:
        orm_mode = True


class MessageNode(Node):
    message: str
    original: Node | None = None
    status: Literal["pending", "sent", "opened"]
    type: str = "message"

    class Config:
        orm_mode = True


class ConditionNode(Node):
    yesNode: Node
    noNode: Node
    condition: str
    type: str = "condition"

    class Config:
        orm_mode = True


class EndNode(Node):
    type: str = "end"

    class Config:
        orm_mode = True


class WorkFlow(BaseModel):
    start_node: StartNode | None = None

    class Config:
        orm_mode = True
