from flask import jsonify
from flask_restful import Resource, reqparse
import hashlib
from app.app import application

parser = reqparse.RequestParser()
parser.add_argument("login", required=True)
parser.add_argument("token", required=True)

TOKEN = "36a6332bedce3afa5584dc3958e31958"


class CheckerToken(Resource):
    def get(self):
        args = parser.parse_args()
        login = args["login"]
        hash_object = hashlib.md5(args["token"].encode())
        hashed_token = hash_object.hexdigest()
        user = application.user_repo.get_persona_by_login(login)
        if not user:
            return jsonify({"error": True, "ans": "there is no user with login {}".format(login)})
        elif user.position.id != 1:  # важный моммент, первой всегда должны быть долдность куратора
            return jsonify({{"error": True, "ans": "wrong position"}})
        elif hashed_token != TOKEN:
            return jsonify({"error": True, "ans": "wrong token"})
        else:
            return jsonify({"error": False, "ans": "success"})
