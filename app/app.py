from flask import Flask
from flask_restful import Api

from data import db_session
from data.db_session import create_session


class DbApp(Flask):
    def __init__(self, *args, **kwargs):
        super(DbApp, self).__init__(*args, **kwargs)

        self.api = Api(self)


db_app = DbApp(__name__, static_folder="./../static")