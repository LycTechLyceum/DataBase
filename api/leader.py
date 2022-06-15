from flask_restful import Resource
from app.app import db_app


class Leader(Resource):
    def post(self, id_user, token, email):
        user = db_app.user_repo.get_persona_by_id(id=id_user)
        if user is None:
            return {"ans": "there is no user with id {}".format(id_user)}
        return {"ans": db_app.cons_repo.set_leader(user=user, email=email, token=token)}
