from database.models import Node
from dependencies import get_db
from routers.node.node_crud import get_node
from routers.schemas import DisplayNodeSchema


def serializer_from_db_to_schema(data: Node) -> DisplayNodeSchema:
    data.status = data.status.value if data.status else None
    data.type = data.type.value
    node = DisplayNodeSchema.from_orm(data)
    return node


if __name__ == '__main__':
    db = next(get_db())
    serializer_from_db_to_schema(get_node(db, 2))
