from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import application

parser = reqparse.RequestParser()
parser.add_argument("id_user", required=True)
parser.add_argument("id_event", required=True)


def get_args():
    args = parser.parse_args()
    try:
        id_user, id_event = int(args["id_user"]), int(args["id_event"])
        if id_user <= 0 or id_event <= 0:
            raise TypeError
    except TypeError:
        return jsonify({"ans": "id must be integer"})
    user = application.user_repo.get_persona_by_id(id_user)
    event = application.event_repo.get_event_by_id(id_event)
    if user is None:
        return True, {"ans": "there is no user with id {}".format(id_user)}
    if event is None:
        return True, {"ans": "there is no event with id {}".format(id_event)}
    else:
        return False, {"user": user, "event": event}


class Curator(Resource):
    def post(self):
        error, ans = get_args()
        if error:
            return jsonify(ans)
        user, event = ans["user"], ans["event"]
        return jsonify({"ans": application.cons_repo.set_curator(user=user, event=event)})

    def delete(self):
        error, ans = get_args()
        if error:
            return jsonify(ans)
        user, event = ans["user"], ans["event"]
        return jsonify({"ans": application.cons_repo.del_curator(user_id=user.id, event_id=event.id)})


