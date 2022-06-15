from flask_restful import Resource
from app.app import db_app


class Leaders(Resource):
    def get(self):
        all_leaders = db_app.cons_repo.get_all_leaders()
        response = {}
        for lead in all_leaders:
            response[lead.personality.id] = {"id": lead.personality.id, "name": lead.personality.name,
                                             "surname": lead.personality.surname, "email": lead.email}
        return response
