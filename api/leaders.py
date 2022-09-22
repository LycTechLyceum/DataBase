from flask import jsonify
from flask_restful import Resource
from app.app import application


class Leaders(Resource):
    def get(self):
        all_leaders = application.cons_repo.get_all_leaders()
        response = {}
        for lead in all_leaders:
            response[lead.personality.id] = {"id": lead.personality.id, "name": lead.personality.name,
                                             "surname": lead.personality.surname, "email": lead.email}
        return jsonify(response)
