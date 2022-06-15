from flask_restful import Resource
from app.app import db_app


class Position(Resource):
    def post(self, pos_name):
        return {"ans": db_app.cons_repo.add_position(pos_name)}

    def get(self, id):
        pos = db_app.cons_repo.get_pos_by_id(id)
        if pos is None:
            return "there is no position with id {}".format(id)
        elif type(pos) == str:
            return {"ans": pos}
        participants = []
        for person in pos.personas:
            participants.append({"id": person.id, "name": person.name, "surname": person.surname})
        return {"id": pos.id, "name": pos.name, "participants": participants}
