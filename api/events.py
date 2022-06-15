from flask import jsonify
from flask_restful import Resource, reqparse

from app.app import db_app


class Events(Resource):
    def get(self):
        d = {}
        for count, event in enumerate(db_app.event_repo.get_all_events()):
            d[count+1] = event.name
        # return jsonify(d)
        return d
