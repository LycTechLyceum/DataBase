import datetime

import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


# таблица, хранящая данные о каждом заказе
class Event(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "events"  #название таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # id - первичный ключ

    id_org = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("organizations.id")) # id организации

    id_customer = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"))  # id заказчика
    id_curator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"))  # id куратора, отвечающего за проект

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # имя
    audience = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # количество человек в аудитории
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today)  # дата создания
    
    # выстраиваем отношения с другими таблицами
    organization = orm.relation("Organization")
    customer = orm.relation("Persona", foreign_keys=[id_customer])
    curator = orm.relation("Persona", foreign_keys=[id_curator])
