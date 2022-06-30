from flask import jsonify
from flask_restful import Resource
from app.app import db_app


class Users(Resource):
    def get(self):
        response = {}
        for persona in db_app.user_repo.get_all_users():
            response[persona.id] = {"name": persona.name, "surname": persona.surname}
        return jsonify(response)
