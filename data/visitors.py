import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица, хранящая все данные о участии программиста в разработке проектов
class Visitor(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'visitors'

    id_visitor = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"),
                                   nullable=False, primary_key=True)
    id_event = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"),
                                 nullable=False, primary_key=True)

    personality = orm.relation("Persona")
    event = orm.relation("Event")
