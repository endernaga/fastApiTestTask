import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.database import SessionLocal, Base, engine
from database.models import Node


class TestDataBase:
    def setup_method(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_type_should_be_one_of_the_choices(self):
        with pytest.raises(Exception) as e:
            test_node = Node(type="asndasd")
            self.session.add(test_node)
            self.session.commit()
            self.session.refresh(test_node)
        test_node_2 = Node(type="start")
        self.session.add(test_node_2)
        self.session.commit()
        self.session.refresh(test_node_2)
        assert test_node_2.type == "start"

    def test_type_cant_be_blank(self):
        with pytest.raises(Exception) as e:
            test_node = Node()
            self.session.add(test_node)
            self.session.commit()
            self.session.refresh(test_node)
