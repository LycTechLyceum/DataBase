from flask import jsonify
from flask_restful import Resource
from app.app import db_app


class Positions(Resource):
    def get(self):
        response = {}
        for pos in db_app.cons_repo.get_all_positions():
            response[pos.id] = pos.name
        return jsonify(response)