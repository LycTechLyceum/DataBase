from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("name", required=False)
parser.add_argument("id", required=False)


class Position(Resource):
    def post(self):
        pos_name = parser.parse_args()["name"]
        return jsonify({"ans": db_app.cons_repo.add_position(pos_name)})

    def get(self):
        try:
            id = int(parser.parse_args()["id"])
            if id <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id must be integer"})
        pos = db_app.cons_repo.get_pos_by_id(id)
        if pos is None:
            return jsonify({"ans": "there is no position with id {}".format(id)})
        elif type(pos) == str:
            return jsonify({"ans": pos})
        participants = []
        for person in pos.personas:
            participants.append({"id": person.id, "name": person.name, "surname": person.surname})
        return jsonify({"id": pos.id, "name": pos.name, "participants": participants})

    def delete(self):
        pos_name = parser.parse_args()["name"]
        return jsonify({"ans": db_app.cons_repo.del_position(pos_name)})

