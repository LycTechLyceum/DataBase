from flask_restful import Resource
from app.app import db_app


class Proger(Resource):
    def post(self, user_id, event_id):
        user = db_app.user_repo.get_persona_by_id(id=user_id)
        event = db_app.event_repo.get_event_by_id(id=event_id)
        if user is None:
            return {"ans": "there is no user with id {}".format(user_id)}
        elif event is None:
            return {"ans": "there is no event with id {}".format(event_id)}
        return {"ans": db_app.cons_repo.set_proger(user=user, event=event)}
