import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица, хранящая все данные о участии программиста в разработке проектов
class Proger(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'progers'

    id_proger = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"),
                                  nullable=False, primary_key=True)
    id_event = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"),
                                 nullable=False, primary_key=True)

    personality = orm.relation("Persona")
    event = orm.relation("Event")
