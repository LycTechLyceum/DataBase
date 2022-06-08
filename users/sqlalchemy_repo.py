import sqlalchemy.exc
from werkzeug.security import generate_password_hash

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


class SQLAlchemyRepo:
    def __init__(self, name):
        db_session.global_init(name)
        self.db_sess = create_session()

    # вернуть персону по её логину
    def get_persona_by_login(self, login):
        return self.db_sess.query(Persona).filter(Persona.login == login).first()

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
                    per.hashed_password = generate_password_hash(password)
                    per.id_position = position.id
                    self.db_sess.add(per)
                    self.db_sess.commit()
                    return "success"
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

    # добавить меропритятие
    def add_event(self, event_name=None, org=None, per_cur=None, per_cus=None):
        try:
            event = Event()
            if type(event_name) != str or type(org) != Organization or \
                    type(per_cur) != Persona or type(per_cus) != Persona:
                raise TypeError
            else:
                event.name = event_name
                event.id_org = org.id
                event.id_customer = per_cus.id
                event.id_curator = per_cur.id
                self.db_sess.add(event)
                self.db_sess.commit()
                return "success"

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # непрвиальные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (name(str)," \
                   " org(Organisation), per_cur(Persona), per_cus(Persona))"

    # добавть организацию если она уникальна
    def add_organization(self, org_name=None):
        try:
            if type(org_name) == str:
                org_existed = self.db_sess.query(Organization).filter(Organization.name == org_name).first()
                if org_existed is None:
                    org = Organization()
                    org.name = org_name
                    self.db_sess.add(org)
                    self.db_sess.commit()
                    return "success"
                else:
                    return "duplicated organization"
            else:
                raise TypeError

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters(org_name(str))"

        # добавить уникальную должность

    def add_position(self, pos_name=None):
        try:
            if type(pos_name) == str:
                pos_existed = self.db_sess.query(Position).filter(Position.name == pos_name)
                if pos_existed is None:
                    pos = Position()
                    pos.name = pos_name
                    self.db_sess.add(pos)
                    self.db_sess.commit()
                    return "success"
                else:
                    return "duplicated position"
            else:
                raise TypeError

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters(pos_name(str))"

        # добавить практиику

    def add_practice(self, practice_name=None):
        try:
            if type(practice_name) == str:
                practice = Practice()
                practice.name = practice_name
                self.db_sess.add(practice)
                self.db_sess.commit()
                return "success"
            else:
                raise TypeError

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters(pos_name(str))"

    # добавть запись о том, что человек посетил событие, при условии уникальности
    def set_visitor(self, user=None, event=None):
        try:
            if type(user) == Persona and type(event) == Event:
                visitor_existed = self.db_sess.query(Visitor).filter(Visitor.id_event == event.id,
                                                                     Visitor.id_visitor == user.id).first()
                if visitor_existed is None:
                    visitor = Visitor()
                    visitor.id_visitor = user.id
                    visitor.id_event = event.id
                    self.db_sess.add(visitor)
                    self.db_sess.commit()
                    return "success"
                else:
                    return "duplicated note"
            else:
                raise TypeError

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (user(Persona), event(Event))"

    # добавить в табличку кураторов запись о курировании
    def set_curator(self, user=None, event=None):
        try:
            if type(user) == Persona and type(event) == Event:
                curator_existed = self.db_sess.query(Curator).filter(Curator.id_curator == user.id,
                                                                     Curator.id_event == event.id).first()
                if curator_existed is None:
                    curator = Curator()
                    curator.id_curator = user.id
                    curator.id_event = event.id
                    self.db_sess.add(curator)
                    self.db_sess.commit()
                    return "success"
                else:
                    return "duplicated note"

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (user(Persona), event(Event))"

    # добавить в табличку заказов запись о заказе
    def set_customer(self, user=None, event=None):
        try:
            if type(user) == Persona and type(event) == Event:
                customer_existed = self.db_sess.query(Customer).filter(Customer.id_customer == user.id,
                                                                       Customer.id_event == event.id).first()
                if customer_existed is None:
                    customer = Customer()
                    customer.id_customer = user.id
                    customer.id_event = event.id
                    self.db_sess.add(customer)
                    self.db_sess.commit()
                    return "success"
                else:
                    return "duplicated note"
            else:
                raise TypeError

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (user(Persona), event(Event))"

    # добавить в табличку активностей разрабов запись о работе над проектом
    def set_proger(self, user=None, event=None):
        try:
            if type(user) == Persona and type(event) == Event:
                proger_existed = self.db_sess.query(Proger).filter(Proger.id_proger == user.id,
                                                                   Proger.id_event == event.id).first()
                if proger_existed is None:
                    proger = Proger()
                    proger.id_proger = user.id
                    proger.id_event = event.id
                    self.db_sess.add(proger)
                    self.db_sess.commit()
                    return "success"
                else:
                    return "duplicated note"

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (user(Persona), event(Event))"

    # добавить данные для лидера
    def set_leader(self, user=None, email=None, token=None):
        try:
            if type(user) == Persona and type(email) == type(token) == str:
                leader_existed = self.db_sess.query(Leader).filter(Leader.id_leader == user.id).first()
                if leader_existed is None:
                    lead = Leader()
                    lead.id_leader = user.id
                    lead.email = email
                    lead.hashed_secret_token = generate_password_hash(token)
                    return "success"
                else:
                    return "user is already a leader"

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (user(Persona), email(str), token(str))"

    def set_visitor_practice(self, visitor=None, practice=None):
        try:
            if type(visitor) == Persona and type(practice) == Practice:
                visitor_practice_existed = self.db_sess.query(VisitorPractice).filter(
                    VisitorPractice.id_practice == practice.id, VisitorPractice.id_visitor == visitor.id).first()
                if visitor_practice_existed is None:
                    visitor_practice = VisitorPractice()
                    visitor_practice.id_visitor = visitor.id
                    visitor_practice.id_practice = practice.id
                    self.db_sess.add(visitor_practice)
                    self.db_sess.commit()
                    return "success"
                else:
                    raise TypeError

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (visitor(Persona), practice(Practice))"
