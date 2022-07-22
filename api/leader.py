from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("id_user", required=True)
parser.add_argument("token", required=True)
parser.add_argument("email", required=True)


class Leader(Resource):
    def post(self):
        args = parser.parse_args()
        try:
            id_user, token, email = int(args["id_user"]), args["token"], args["email"]
            if id_user <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id user must be integer"})
        user = db_app.user_repo.get_persona_by_id(id=id_user)
        if user is None:
            return jsonify({"ans": "there is no user with id {}".format(id_user)})
        return jsonify({"ans": db_app.cons_repo.set_leader(user=user, email=email, token=token)})
