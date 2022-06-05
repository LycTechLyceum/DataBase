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
    hashed_secret_token = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String)
    personality = orm.relation("Persona")

    def set_hash(self, token):
        self.hashed_secret_token = generate_password_hash(token)

    def check_hash(self, token):
        return check_password_hash(self.hashed_secret_token, token)
