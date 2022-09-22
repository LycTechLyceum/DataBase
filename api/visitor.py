from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import application

parser = reqparse.RequestParser()
parser.add_argument("id_user", required=True)
parser.add_argument("id_event", required=True)


class Visitor(Resource):
    def delete(self):
        args = parser.parse_args()
        try:
            id_user, id_event = int(args["id_user"]), int(args["id_event"])
            if id_user <= 0 or id_event <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id must be integer"})
        user = application.user_repo.get_persona_by_id(id=id_user)
        event = application.event_repo.get_event_by_id(id=id_event)
        if user is None:
            return jsonify({"ans": "there is no user with id {}".format(id_user)})
        elif event is None:
            return jsonify({"ans": "there is no event with id {}".format(id_event)})
        return jsonify({"ans": application.cons_repo.delete_visitor(user_id=id_user, event_id=id_event)})

    def post(self):
        args = parser.parse_args()
        try:
            id_user, id_event = int(args["id_user"]), int(args["id_event"])
            if id_user <= 0 or id_event <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id must be integer"})
        user = application.user_repo.get_persona_by_id(id=id_user)
        event = application.event_repo.get_event_by_id(id=id_event)
        if user is None:
            return jsonify({"ans": "there is no user with id {}".format(id_user)})
        elif event is None:
            return jsonify({"ans": "there is no event with id {}".format(id_event)})
        return jsonify({"ans": application.cons_repo.set_visitor(user=user, event=event)})