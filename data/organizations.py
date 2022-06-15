import datetime

import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


# таблица, содержащая все организации, которые делали заказы
class Organization(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'organizations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    audience = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today)

    events = orm.relation("Event", back_populates="organization")
