import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица, в которой хранятся все заказчики и преокты, которые они заказывали
class Customer(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'customers'

    id_customer = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"),
                                    nullable=False, primary_key=True)
    id_event = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"),
                                 nullable=False, primary_key=True)

    personality = orm.relation("Persona")
    event = orm.relation("Event")
