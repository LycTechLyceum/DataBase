from flask import jsonify
from flask_restful import Resource
from app.app import application


class Users(Resource):
    def get(self):
        response = {}
        for persona in application.user_repo.get_all_users():
            response[persona.id] = {"name": persona.name, "surname": persona.surname}
        return jsonify(response)
