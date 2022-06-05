import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица со всеми возможными должностями
class Position(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'positions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, unique=True)

    personas = orm.relation("Persona", back_populates="position")
