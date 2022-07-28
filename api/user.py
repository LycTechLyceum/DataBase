from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("id", required=False)
parser.add_argument("name", required=False)
parser.add_argument("surname", required=False)
parser.add_argument("grade", required=False)
parser.add_argument("login", required=False)
parser.add_argument("password", required=False)
parser.add_argument("id_pos", required=False)


class User(Resource):
    def get(self):
        args = parser.parse_args()
        try:
            id = int(args["id"])
            if id <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id must be integer"})
        persona = db_app.user_repo.get_persona_by_id(id)
        if persona is None:
            return {"ans": "there is no user with id {}".format(id)}
        elif type(persona) == str:
            return {"ans": persona}

        response = {"id": persona.id, "name": persona.name, "surname": persona.surname, "grade": persona.grade,
                    "login": persona.login, "position": {"id": persona.id_position, "name": persona.position.name},
                    "date": str(persona.created_date.day) + "." + str(persona.created_date.month) +
                    "." + str(persona.created_date.year)}
        return jsonify(response)

    def post(self):
        args = parser.parse_args()

        name = args["name"]
        surname = args["surname"]
        grade = args["grade"]
        login = args["login"]
        password = args["password"]
        try:
            id_pos = int(args["id_pos"])
            if id_pos <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id position must be integer"})

        pos = db_app.cons_repo.get_pos_by_id(id_pos)
        if pos is None:
            return jsonify({"ans": "there is no position with id {}".format(id_pos)})
        elif type(pos) == str:
            return jsonify({"ans": pos})

        add_user_callback = db_app.user_repo.add_user(
            name=name,
            surname=surname,
            grade=grade,
            login=login,
            password=password,
            position=pos
        )
        return jsonify({"ans": add_user_callback})
