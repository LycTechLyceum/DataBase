import sqlalchemy.exc
import hashlib

from data import db_session
from data.curators import Curator
from data.customers import Customer
from data.db_session import create_session
from data.events import Event
from data.leaders import Leader
from data.organizations import Organization
from data.personas import Persona
from data.positions import Position
from data.practices import Practice
from data.progers import Proger
from data.visitors import Visitor

# класс, взаимодейсвующей с базой данных, все добавления / изменения / удаления
# должны производиться ТОЛЬКО в нём, тк главная наша задача - не уронить к чёрту сервер
# а все возможные ошибки ( или почти все >:) ) в работе с алхимией ловятся тут
from data.visitors_practices import VisitorPractice


class SQLAlchemyUserRepo:
    def __init__(self, name):
        db_session.global_init(name)
        self.db_sess = create_session()

    # вернуть персону по её логину
    def get_persona_by_login(self, login):
        return self.db_sess.query(Persona).filter(Persona.login == login).first()

    def get_persona_by_id(self, id):
        try:
            if type(id) == int:
                return self.db_sess.query(Persona).filter(Persona.id == id).first()
            else:
                raise TypeError
        except TypeError:
            return "wrong type one of the parameters(id(int))"

    def get_all_users(self):
        return self.db_sess.query(Persona).all()

    # добавть пользователя при условии, что логин уникален
    def add_user(self, name=None, surname=None, grade=None, login=None, password=None, position=None):
        try:
            per = Persona()
            already_created_persona = self.get_persona_by_login(login)
            if already_created_persona is None:
                if type(name) == type(surname) == type(grade) == type(login) == type(password) == str \
                        and type(position) == Position:
                    per.name = name
                    per.surname = surname
                    per.grade = grade
                    per.login = login

                    hash_object = hashlib.md5(password.encode())
                    per.hashed_password = hash_object.hexdigest()
                    per.id_position = position.id
                    self.db_sess.add(per)
                    self.db_sess.commit()
                    return {"ans": "success", "heashed_password": per.hashed_password}
                else:
                    raise TypeError
            else:
                return "duplicated login"

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (name(str), surname(str)," \
                   " grade(str), login(str), password(str), position(Position)"

    def delete_user(self, id):
        self.db_sess.query(Persona).filter(Persona.id == id).delete()
        self.db_sess.commit()
        return "success"








