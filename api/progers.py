from flask_restful import Resource
from app.app import db_app


class Progers(Resource):
    def get(self):
        all_progers = db_app.cons_repo.get_all_progers()
        # sorted(all_progers, key=lambda x: x.personality.login)
        response = {}
        for proger in all_progers:
            if proger.id_proger not in response.keys():
                response[proger.id_proger] = {"id": proger.personality.id, "name": proger.personality.name,
                                              "surname": proger.personality.surname,
                                              "events": [{"id": proger.event.id, "name": proger.event.name}]}
            else:
                response[proger.id_proger]["events"].append({"id": proger.event.id, "name": proger.event.name})
        return response
