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
from data.visitors_practices import VisitorPractice
from data.stateless_events import StatelessEvents


class SQLAlchemyConnectionRepo:
    def __init__(self, name):
        db_session.global_init(name)
        self.db_sess = create_session()

    def get_customers_by_org(self, org=None):
        try:
            if type(org) == Organization:
                needed_events = self.db_sess.query(Event).filter(Event.organization == org).all()
                events_id = [event.id for event in needed_events]
                return self.db_sess.query(Customer).filter(Customer.id_event.in_(events_id)).all()
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
            return "wrong type one of the parameters(org(Organization))"

    def get_progers_by_event_id(self, id=None):
        try:
            if type(id) == int:
                event = self.db_sess.query(Event).filter(Event.id == id).first()
                if event is not None:
                    progres = self.db_sess.query(Proger).filter(Proger.id_event == id).all()
                    return progres
                else:
                    return "there is no event with id {}".format(id)
        except TypeError:
            return "wrong type one of the parameters(id(int))"

    def get_visitors_by_event_id(self, id=None):
        try:
            if type(id) == int:
                event = self.db_sess.query(Event).filter(Event.id == id).first()
                if event is not None:
                    visitors = self.db_sess.query(Visitor).filter(Visitor.id_event == id).all()
                    return visitors
                else:
                    return "there is no event with id {}".format(id)
        except TypeError:
            return "wrong type one of the parameters(id(int))"

    def get_pos_by_id(self, id):
        try:
            if type(id) == int:
                return self.db_sess.query(Position).filter(Position.id == id).first()
            else:
                raise TypeError
        except TypeError:
            return "wrong type one of the parameters(id(int))"

    def get_all_positions(self):
        return self.db_sess.query(Position).all()

    def add_position(self, pos_name=None):
        try:
            if type(pos_name) == str:
                pos_existed = self.db_sess.query(Position).filter(Position.name == pos_name).first()
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

    def del_position(self, pos_name=None):
        pos_existed = self.db_sess.query(Position).filter(Position.name == pos_name).first()
        if pos_existed is None:
            return "no position with name {}".format(pos_name)
        self.db_sess.query(Position).filter(Position.name == pos_name).delete()
        self.db_sess.commit()
        return "success"

    def get_all_practices(self):
        return self.db_sess.query(Practice).all()

    def get_all_progers(self):
        return self.db_sess.query(Proger).all()

    def get_all_visitors(self):
        return self.db_sess.query(Visitor).all()

    def get_all_visitors_practices(self):
        return self.db_sess.query(VisitorPractice).all()

    def get_all_leaders(self):
        return self.db_sess.query(Leader).all()

    def get_all_customers(self):
        return self.db_sess.query(Customer).all()

    def get_all_curators(self):
        return self.db_sess.query(Curator).all()

    def get_practice_by_id(self, id=None):
        try:
            if type(id) == int:
                return self.db_sess.query(Practice).filter(Practice.id == id).first()
            else:
                raise TypeError
        except TypeError:
            return "wrong type one of the parameters(id(int))"

    def add_practice(self, practice_org=None, practice_name=None):
        try:
            if type(practice_name) == str and type(practice_org) == Persona:
                practice = Practice()
                practice.name = practice_name
                practice.id_org = practice_org.id
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
            return "wrong type one of the parameters(practice_org(Persona), pos_name(str))"

    def delete_practice(self, practice_id):
        self.db_sess.query(VisitorPractice).filter(VisitorPractice.id_practice == practice_id).delete()
        self.db_sess.query(Practice).filter(Practice.id == practice_id).delete()
        self.db_sess.commit()
        return "success"

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

    def delete_proger(self, user=None, event=None):
        try:
            if type(user) != Persona or type(event) != Event:
                raise TypeError
            self.db_sess.query(Proger).filter(Proger.id_proger == user.id).delete()
            self.db_sess.commit()
            return "success"

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters (user(Persona), event(Event))"

    # добавть запись о том, что человек посетил событие, при условии уникальности
    def set_visitor(self, user=None, event=None):
        try:
            if type(user) == Persona and type(event) == Event:
                visitor_existed = self.db_sess.query(Visitor).filter(Visitor.id_event == event.id,
                                                                     Visitor.id_visitor == user.id).first()
                event.audience += 1
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

    def delete_visitor(self, user_id, event_id):
        self.db_sess.query(Visitor).filter(Visitor.id_visitor == user_id, Visitor.id_event == event_id).delete()
        self.db_sess.commit()
        return "success"

    # добавить посетителя практикума
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
            return "wrong type one of the parameters (visitor(Persona), practice(Practice))"

    def delete_visitor_practice(self, user_id, practice_id):
        self.db_sess.query(VisitorPractice).filter(VisitorPractice.id_practice == practice_id,
                                                   VisitorPractice.id_visitor == user_id)
        self.db_sess.commit()
        return "success"

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
                    self.db_sess.add(lead)
                    self.db_sess.commit()
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

    def del_lead(self, user_id):
        self.db_sess.query(Leader).filter(Leader.id_leader == user_id).delete()
        self.db_sess.commit()
        return "success"

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

    def del_customer(self, user_id=None, event_id=None):
        self.db_sess.query(Customer).filter(Customer.id_customer == user_id, Customer.id_event == event_id).delete()
        self.db_sess.commit()
        return "success"

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

    def del_curator(self, user_id=None, event_id=None):
        self.db_sess.query(Curator).filter(Curator.id_curator == user_id, Curator.id_event == event_id).delete()
        self.db_sess.commit()
        return "success"

    def get_st_event_by_id(self, id):
        return self.db_sess.query(StatelessEvents).filter(StatelessEvents.id == id).first()

    def get_all_st_events(self):
        return self.db_sess.query(StatelessEvents).all()

    def add_stateless_events(self, title, description, contact, user_id):
        st_event = StatelessEvents()
        st_event.id_customer = user_id
        st_event.title = title
        st_event.description = description
        st_event.contact = contact
        self.db_sess.add(st_event)
        self.db_sess.commit()
        return "success"

    def delete_stateless_events(self, id):
        self.db_sess.query(StatelessEvents).filter(StatelessEvents.id == id).delete()
        self.db_sess.commit()
        return "success"

