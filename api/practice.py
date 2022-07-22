from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import db_app


parser = reqparse.RequestParser()
parser.add_argument("id_org", required=False)
parser.add_argument("name", required=False)
parser.add_argument("id", required=False)


class Practice(Resource):
    def post(self):
        args = parser.parse_args()
        try:
            id_org, name = int(args["id_org"]), args["name"]
            if id_org <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id org must be integer"})
        org = db_app.user_repo.get_persona_by_id(id=id_org)
        if org is None:
            return jsonify({"ans": "there is no user with id {}".format(id_org)})
        return jsonify({"ans": db_app.cons_repo.add_practice(practice_org=org, practice_name=name)})

    def get(self):
        try:
            print(parser.parse_args()["id"])
            id_practice = int(parser.parse_args()["id"])
            if id_practice <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id practice must be integer"})
        practice = db_app.cons_repo.get_practice_by_id(id_practice)
        if practice is None:
            return jsonify({"ans": "threr is no practice with id {}".format(id_practice)})
        elif type(practice) == str:
            return jsonify({"ans": practice})
        visitors = []
        for visitor_practice in practice.visitors:
            persona = visitor_practice.personality
            visitors.append({"id": persona.id, "name": persona.name, "surname": persona.surname})
        org = {"id": practice.organizer.id, "name": practice.organizer.name, "surname": practice.organizer.surname}
        response = {"id": practice.id, "name": practice.name, "organizer": org, "visitors": visitors}
        return jsonify(response)
