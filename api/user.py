from flask_restful import Resource
from app.app import db_app


class User(Resource):
    def get(self, id):
        persona = db_app.user_repo.get_persona_by_id(id)
        if persona is None:
            return {"ans": "there is no user with id {}".format(id)}
        elif type(persona) == str:
            return {"ans": persona}

        response = {"id": persona.id, "name": persona.name, "surname": persona.surname, "grade": persona.grade,
                    "login": persona.login, "position": {"id": persona.id_position, "name": persona.position.name},
                    "date": str(persona.created_date.day) + "." + str(persona.created_date.month) +
                    "." + str(persona.created_date.year)}
        return response

    def post(self, name=None, surname=None, grade=None, login=None, password=None, id_pos=None):
        pos = db_app.cons_repo.get_pos_by_id(id_pos)
        if pos is None:
            return {"ans": "there is no position with id {}".format(id_pos)}
        elif type(pos) == str:
            return {"ans": pos}
        add_user_callback = db_app.user_repo.add_user(
            name=name,
            surname=surname,
            grade=grade,
            login=login,
            password=password,
            position=pos
        )
        return {"ans": add_user_callback}
