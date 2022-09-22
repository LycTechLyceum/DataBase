from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import application

parser = reqparse.RequestParser()
parser.add_argument("id_user", required=True)
parser.add_argument("id_practice", required=True)


class VisitorPractice(Resource):
    def delete(self):
        args = parser.parse_args()
        try:
            id_user, id_practice = int(args["id_user"]), int(args["id_practice"])
            if id_user <= 0 or id_practice <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "all id must be integers"})
        user = application.user_repo.get_persona_by_id(id=id_user)
        practice = application.cons_repo.get_practice_by_id(id=id_practice)
        if user is None:
            return jsonify({"ans": "there is no user with id {}".format(id_user)})
        elif practice is None:
            return jsonify({"ans": "there is no practice with id {}".format(id_practice)})
        return jsonify({"ans": application.cons_repo.delete_visitor_practice(id_user, id_practice)})

    def post(self):
        args = parser.parse_args()
        try:
            id_user, id_practice = int(args["id_user"]), int(args["id_practice"])
            if id_user <= 0 or id_practice <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "all id must be integers"})
        user = application.user_repo.get_persona_by_id(id=id_user)
        practice = application.cons_repo.get_practice_by_id(id=id_practice)
        if user is None:
            return jsonify({"ans": "there is no user with id {}".format(id_user)})
        elif practice is None:
            return jsonify({"ans": "there is no practice with id {}".format(id_practice)})
        return jsonify({"ans": application.cons_repo.set_visitor_practice(visitor=user, practice=practice)})
