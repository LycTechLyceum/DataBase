import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица, в которой хранятся записи кураторов каждого заказа
class Curator(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'curators'

    id_curator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"),
                                   nullable=False, primary_key=True)
    id_event = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"),
                                 nullable=False, primary_key=True)

    personality = orm.relation("Persona")
    event = orm.relation("Event")
