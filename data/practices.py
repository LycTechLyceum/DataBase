import datetime

import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица со всеми практиками
class Practice(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'practices'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today)

    visitors = orm.relation("VisitorPractice")
