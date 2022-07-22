import sqlalchemy.exc

from data import db_session
from data.curators import Curator
from data.db_session import create_session
from data.events import Event
from data.organizations import Organization
from data.personas import Persona


class SQLAlchemyEventRepo:
    def __init__(self, name):
        db_session.global_init(name)
        self.db_sess = create_session()

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

    def get_event_by_id(self, id=None):
        try:
            if type(id) == int:
                return self.db_sess.query(Event).filter(Event.id == id).first()
            else:
                raise TypeError
        except TypeError:
            return "wrong type one of the parameters(id(int))"

    def get_events_by_org_name(self, name=None):
        org = self.db_sess.query(Organization).filter(Organization.name == name).first()
        print(org)
        return org.events
        # try:
        #     if type(name) == str:
        #         return self.db_sess.query(Event).filter(Event.organization.name == name).all()
        #     else:
        #         raise TypeError
        # except TypeError:
        #     return "wrong type one of the parameters(id(int))"

    def get_all_events(self):
        return self.db_sess.query(Event).all()
