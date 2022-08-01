from flask import jsonify
from flask_restful import Resource, reqparse
import hashlib
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("login", required=True)
parser.add_argument("password", required=True)


class Checker(Resource):
    def get(self):
        args = parser.parse_args()
        login = args["login"]
        hash_object = hashlib.md5(args["password"].encode())
        hashed_password = hash_object.hexdigest()
        user = db_app.user_repo.get_persona_by_login(login)
        if user is None:
            return jsonify({"ans": False, "password": args["password"], "hashed password": hashed_password})
        if hashed_password != user.hashed_password:
            return jsonify({"ans": False, "password": args["password"], "hashed password": hashed_password})
        else:
            return jsonify({"ans": True, "password": args["password"], "hashed password": hashed_password})
