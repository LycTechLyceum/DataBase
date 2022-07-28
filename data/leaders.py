import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# таблица, содержащая email-ы и хэши глав
class Leader(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'leaders'

    id_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("personas.id"),
                                  nullable=False, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    personality = orm.relation("Persona")

