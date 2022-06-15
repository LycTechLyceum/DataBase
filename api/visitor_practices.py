from flask_restful import Resource
from app.app import db_app


class VisitorPractice(Resource):
    def post(self, id_user, id_practice):
        user = db_app.user_repo.get_persona_by_id(id=id_user)
        practice = db_app.cons_repo.get_practice_by_id(id=id_practice)
        if user is None:
            return {"ans": "there is no user with id {}".format(id_user)}
        elif practice is None:
            return {"ans": "there is no practice with id {}".format(id_practice)}
        return {"ans": db_app.cons_repo.set_visitor_practice(visitor=user, practice=practice)}
