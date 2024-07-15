import abc
from typing import Literal, Optional, Union

from pydantic import BaseModel


class Node(BaseModel, abc.ABC):
    type: str
    pass


class StartNode(Node):
    original: Optional[Union[Node, int]] = None
    type: str = "start"

    class Config:
        orm_mode = True


class StartNodeCreate(Node):
    type: str = "start"


class MessageNode(Node):
    message: str
    original: Node | None | int = None
    status: Literal["pending", "sent", "opened"]
    type: str = "message"

    class Config:
        orm_mode = True


class ConditionNode(Node):
    yesNode: Node | int
    noNode: Node | int
    condition: str
    type: str = "condition"

    class Config:
        orm_mode = True


class EndNode(Node):
    type: str = "end"

    class Config:
        orm_mode = True


class WorkFlow(BaseModel):
    start_node: Optional[Union[StartNodeCreate, int]] = None

    class Config:
        orm_mode = True


class WorkFlowDisplay(BaseModel):
    id: int
    start_node_id: Optional[Union[StartNode, int]] = None

    class Config:
        orm_mode = True
