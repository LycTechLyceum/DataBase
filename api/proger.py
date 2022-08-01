from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("id_user", required=True)
parser.add_argument("id_event", required=True)


class Proger(Resource):
    def delete(self):
        args = parser.parse_args()
        try:
            user_id, event_id = int(args["id_user"]), int(args["id_event"])
            if user_id <= 0 or event_id <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "all id must be integers"})
        user = db_app.user_repo.get_persona_by_id(id=user_id)
        event = db_app.event_repo.get_event_by_id(id=event_id)
        if user is None:
            return jsonify({"ans": "there is no user with id {}".format(user_id)})
        elif event is None:
            return jsonify({"ans": "there is no event with id {}".format(event_id)})
        return jsonify({"ans": db_app.cons_repo.delete_proger(user=user, event=event)})

    def post(self):
        args = parser.parse_args()
        try:
            user_id, event_id = int(args["id_user"]), int(args["id_event"])
            if user_id <= 0 or event_id <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "all id must be integers"})
        user = db_app.user_repo.get_persona_by_id(id=user_id)
        event = db_app.event_repo.get_event_by_id(id=event_id)
        if user is None:
            return jsonify({"ans": "there is no user with id {}".format(user_id)})
        elif event is None:
            return jsonify({"ans": "there is no event with id {}".format(event_id)})
        return jsonify({"ans": db_app.cons_repo.set_proger(user=user, event=event)})
