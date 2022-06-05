import datetime

import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица с общими данными о всех пользователях
class Persona(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'personas'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    grade = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today, nullable=False)

    id_position = sqlalchemy.Column(sqlalchemy.ForeignKey("positions.id"), nullable=False)

    position = orm.relation("Position", back_populates="personas")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
