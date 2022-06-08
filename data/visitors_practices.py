import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица
class VisitorPractice(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'visitors_practices'

    id_visitor = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"),
                                   nullable=False, primary_key=True)
    id_practice = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("practices.id"),
                                    nullable=False, primary_key=True)

    personality = orm.relation("Persona")
    practice = orm.relation("Practice", overlaps="visitors")
