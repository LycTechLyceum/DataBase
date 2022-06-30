from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("id_user", required=True)
parser.add_argument("id_event", required=True)


class Customer(Resource):
    def post(self):
        args = parser.parse_args()
        try:
            id_user, id_event = args["id_user"], args["id_event"]
            if id_user <= 0 or id_event <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id must be integer"})
        user = db_app.user_repo.get_persona_by_id(id_user)
        event = db_app.event_repo.get_event_by_id(id_event)
        if user is None:
            return jsonify({"ans": "there is no user with id {}".format(id_user)})
        if event is None:
            return jsonify({"ans": "there is no practice with id {}".format(id_event)})
        return jsonify({"ans": db_app.cons_repo.set_customer(user=user, event=event)})
