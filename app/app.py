from flask import Flask
from flask_restful import Api

from repo.sqlalchemy_connections_repo import SQLAlchemyConnectionRepo
from repo.sqlalchemy_events_repo import SQLAlchemyEventRepo
from repo.sqlalchemy_organisations_repo import SQLAlchemyOrganizationRepo
from repo.sqlalchemy_user_repo import SQLAlchemyUserRepo


class DbApp(Flask):
    def __init__(self, *args, **kwargs):
        super(DbApp, self).__init__(*args, **kwargs)
        db_way = "db/db_proglyc.db"
        self.user_repo = SQLAlchemyUserRepo(db_way)
        self.org_repo = SQLAlchemyOrganizationRepo(db_way)
        self.cons_repo = SQLAlchemyConnectionRepo(db_way)
        self.event_repo = SQLAlchemyEventRepo(db_way)
        self.secret_key = "super-secret"
        self.api = Api(self)


db_app = DbApp(__name__, static_folder="./../static")


@db_app.errorhandler(404)
def not_found():
    return 'Ой! Что-то пошло не так. Скорее всего, такой страницы не существует :(', 404
