from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("login", required=True)
parser.add_argument("token", required=True)

TOKEN = "pbkdf2:sha256:260000$UJSnqcZex6sOIQwu$3b2c825b818d5c9012562b35314b7c74e12db059dbdad76a0db882f7fc5f0f21"


class CheckerToken(Resource):
    def get(self):
        args = parser.parse_args()
        login = args["login"]
        hashed_token = generate_password_hash(args["token"])
        user = db_app.user_repo.get_persona_by_login(login)
        if not user:
            return jsonify({"error": True, "ans": "there is no user with login {}".format(login)})
        elif user.position.id != 1:  # важный моммент, первой всегда должны быть долдность куратора
            return jsonify({{"error": True, "ans": "wrong position"}})
        elif hashed_token != TOKEN:
            return jsonify({{"error": True, "ans": "wrong token"}})
        else:
            return jsonify({{"error": False, "ans": "success"}})
