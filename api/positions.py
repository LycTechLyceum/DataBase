from flask import jsonify
from flask_restful import Resource
from app.app import application


class Positions(Resource):
    def get(self):
        response = {}
        for pos in application.cons_repo.get_all_positions():
            response[pos.id] = pos.name
        return jsonify(response)
