from flask import jsonify
from flask_restful import Resource
from app.app import db_app


class VisitorsPractices(Resource):
    def get(self):
        all_visitors = db_app.cons_repo.get_all_visitors_practices()
        response = {}
        for visitor in all_visitors:
            if visitor.id_visitor not in response.keys():
                response[visitor.id_visitor] = {"id": visitor.personality.id, "name": visitor.personality.name,
                                                "surname": visitor.personality.surname,
                                                "practice": [{"id": visitor.practice.id, "name": visitor.practice.name}]}
            else:
                response[visitor.id_visitor]["practice"].append({"id": visitor.practice.id,
                                                                 "name": visitor.practice.name})
        return jsonify(response)
