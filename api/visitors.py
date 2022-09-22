from flask import jsonify
from flask_restful import Resource
from app.app import application


class Visitors(Resource):
    def get(self):
        all_visitors = application.cons_repo.get_all_visitors()
        response = {}
        for visitor in all_visitors:
            if visitor.id_visitor not in response.keys():
                response[visitor.id_visitor] = {"id": visitor.personality.id, "name": visitor.personality.name,
                                                "surname": visitor.personality.surname,
                                                "events": [{"id": visitor.event.id, "name": visitor.event.name}]}
            else:
                response[visitor.id_visitor]["events"].append({"id": visitor.event.id, "name": visitor.event.name})
        return jsonify(response)
