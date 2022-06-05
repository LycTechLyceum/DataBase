import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


# таблица, содержащая все организауии, которые делали заказы
class Organization(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'organizations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    audience = sqlalchemy.Column(sqlalchemy.Integer)

    events = orm.relation("Event", back_populates="organization")
