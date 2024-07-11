from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, remote
from sqlalchemy_utils import ChoiceType

from .database import Base


class Node(Base):
    TYPES = [
        ("start", "start"),
        ("condition", "condition"),
        ("message", "message"),
        ("end", "end")
    ]
    STATUS = [
        ("pending", "pending"),
        ("sent", "sent"),
        ("opened", "opened")
    ]
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, name="id")
    type = Column(ChoiceType(TYPES), nullable=False, name="type")
    message = Column(String, nullable=True)
    status = Column(ChoiceType(STATUS), nullable=True)
    condition = Column(String, nullable=True)
    original_id = Column(Integer, ForeignKey("nodes.id"),
                         nullable=True)  # OneToMany ref one messsage can have many parent's node TODO: only if kind == "condtion or message"

    original = relationship("Node", remote_side=[id], backref=backref("children", uselist=True),
                            foreign_keys=[original_id])

    yesNode_id = Column(Integer, ForeignKey("nodes.id"),
                        nullable=True)  # OneToOne ref TODO: only if kind == "condition"
    noNode_id = Column(Integer, ForeignKey("nodes.id"), nullable=True)  # OneToOne ref

    yesNode = relationship("Node", foreign_keys=[yesNode_id], backref=backref("yesNode_parent", uselist=False),
                           remote_side=[id])
    noNode = relationship("Node", foreign_keys=[noNode_id], backref=backref("noNode_parent", uselist=False),
                          remote_side=[id])


class WorkFlow(Base):
    __tablename__ = "Workflow"

    id = Column(Integer, primary_key=True)

    start_node_id = Column(Integer, ForeignKey("nodes.id"), nullable=True)
    start_node = relationship("Node", backref=backref("workflow", uselist=False),
                              primaryjoin="WorkFlow.start_node_id == Node.id",
                              remote_side=[Node.id])
