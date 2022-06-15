from flask_restful import Resource
from app.app import db_app


class Curators(Resource):
    def get(self):
        all_curators = db_app.cons_repo.get_all_curators()
        response = {}
        for curator in all_curators:
            if curator.personality.id not in response.keys():
                response[curator.personality.id] = {"id": curator.personality.id, "name": curator.personality.name,
                                                     "surname": curator.personality.surname,
                                                     "events": [{"id": curator.event.id, "name": curator.event.name}]}
            else:
                response[curator.personality.id]["events"].append({"id": curator.event.id,
                                                                    "name": curator.event.name})
        return response
