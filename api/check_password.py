from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("login", required=True)
parser.add_argument("password", required=True)


class Checker(Resource):
    def get(self):
        args = parser.parse_args()
        login = args["login"]
        hashed_password = generate_password_hash(args["password"])
        user = db_app.user_repo.get_persona_by_login(login)
        if not user:
            return jsonify({"ans": False})
        elif hashed_password != user.hashed_password:
            return jsonify({{"ans": False}})
        else:
            return jsonify({{"ans": True}})
