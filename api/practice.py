from flask_restful import Resource
from app.app import db_app


class Practice(Resource):
    def post(self, id_org, name):
        org = db_app.user_repo.get_persona_by_id(id=id_org)
        if org is None:
            return {"ans": "there is no user with id {}".format(id_org)}
        return {"ans": db_app.cons_repo.add_practice(practice_org=org, practice_name=name)}

    def get(self, id_practice):
        practice = db_app.cons_repo.get_practice_by_id(id_practice)
        if practice is None:
            return {"ans": "threr is no practice with id {}".format(id_practice)}
        elif type(practice) == str:
            return {"ans": practice}
        visitors = []
        for visitor_practice in practice.visitors:
            persona = visitor_practice.personality
            visitors.append({"id": persona.id, "name": persona.name, "surname": persona.surname})
        org = {"id": practice.organizer.id, "name": practice.organizer.name, "surname": practice.organizer.surname}
        response = {"id": practice.id, "name": practice.name, "organizer": org, "visitors": visitors}
        return response
