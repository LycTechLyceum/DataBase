from flask import jsonify
from flask_restful import Resource
from app.app import db_app


class Practices(Resource):
    def get(self):
        response = {}
        for practice in db_app.cons_repo.get_all_practices():
            response[practice.id] = {practice.name, practice.date, practice.id}
        return jsonify(response)
