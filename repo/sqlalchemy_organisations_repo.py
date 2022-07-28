import sqlalchemy.exc

from data import db_session
from data.db_session import create_session
from data.organizations import Organization


class SQLAlchemyOrganizationRepo:
    def __init__(self, name):
        db_session.global_init(name)
        self.db_sess = create_session()

    def get_org_by_id(self, id=None):
        try:
            if type(id) != int:
                raise TypeError
            return self.db_sess.query(Organization).filter(Organization.id == id).first()
        except TypeError:
            return "wrong type one of the parameters(id(int))"

    def get_org_by_name(self, name=None):
        try:
            if type(name) == str:
                return self.db_sess.query(Organization).filter(Organization.name == name).first(), None
            else:
                raise TypeError
        except TypeError:
            return None, "wrong type one of the parameters(name(str))"

    # добавть организацию если она уникальна
    def add_organization(self, org_name=None):
        try:
            org_existed, error = self.get_org_by_name(org_name)
            if org_existed is None and error is None:
                org = Organization()
                org.name = org_name
                self.db_sess.add(org)
                self.db_sess.commit()
                return "success"
            elif org_existed is None and error is not None:
                return error
            else:
                return "duplicated organization"

        # что-то пошло не так при добавлении sqlalchemy-ей в бд
        except sqlalchemy.exc.IntegrityError as error:
            return "integrity error: {}".format(error)
        # у кого-то параметра не задан атрибут
        except sqlalchemy.exc.PendingRollbackError as error:
            return "some parameter doesn't have needed attribute: {}".format(error)
        # неправильные типы переданных переменных
        except TypeError:
            return "wrong type one of the parameters(org_name(str))"

    # возврящает все организации
    def get_all_organizations(self):
        return self.db_sess.query(Organization).all()

    def del_org(self, id):
        self.db_sess.query(Organization).filter(Organization.id == id).delete()
        self.db_sess.commit()
        return "success"
