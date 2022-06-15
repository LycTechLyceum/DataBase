from flask_restful import Resource
from app.app import db_app


class Customer(Resource):
    def post(self, id_user, id_event):
        user = db_app.user_repo.get_persona_by_id(id_user)
        event = db_app.event_repo.get_event_by_id(id_event)
        if user is None:
            return {"ans": "there is no user with id {}".format(id_user)}
        if event is None:
            return {"ans": "there is no practice with id {}".format(id_event)}
        return {"ans": db_app.cons_repo.set_customer(user=user, event=event)}
