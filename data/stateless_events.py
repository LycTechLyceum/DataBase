import datetime

import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


# таблица, содержащая все организации, которые делали заказы
class StatelessEvents(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'stateless-events'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    id_customer = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"))

    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=False)
    contact = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today)

    customer = orm.relation("Persona", foreign_keys=[id_customer])
