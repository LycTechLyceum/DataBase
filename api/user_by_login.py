from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import application

parser = reqparse.RequestParser()
parser.add_argument("login", required=True)


class UserData(Resource):
    def get(self):
        args = parser.parse_args()
        login = args["login"]
        persona = application.user_repo.get_persona_by_login(login)
        if persona is None:
            return {"ans": "there is no user with login {}".format(login)}
        elif type(persona) == str:
            return {"ans": persona}

        response = {"id": persona.id, "name": persona.name, "surname": persona.surname, "grade": persona.grade,
                    "login": persona.login, "position": {"id": persona.id_position, "name": persona.position.name},
                    "date": str(persona.created_date.day) + "." + str(persona.created_date.month) +
                    "." + str(persona.created_date.year)}
        return jsonify(response)

