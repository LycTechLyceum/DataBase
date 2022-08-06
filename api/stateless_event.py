from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("id_user", required=False)
parser.add_argument("title", required=False)
parser.add_argument("description", required=False)
parser.add_argument("contact", required=False)
parser.add_argument("st_event_id", required=False)


def st_event_controller():
    args = parser.parse_args()
    try:
        user_id, title, description, contact = int(args["id_user"]), args["title"], \
                                               args["description"], args["contact"]
        if user_id <= 0:
            raise TypeError
    except TypeError:
        return jsonify({"ans": "all id must be integers"})
    except Exception:
        return jsonify({"ans": "error, try to check all params"})
    user = db_app.user_repo.get_persona_by_id(id=user_id)
    if user is None:
        return True, {"ans": "there is no user with id {}".format(user_id)}
    return False, [title, description, contact, user_id]


class StatelessEvent(Resource):
    def delete(self):
        args = parser.parse_args()
        try:
            st_event_id = int(args["st_event_id"])
        except TypeError:
            return jsonify({"ans": "all id must be integers"})
        except Exception:
            return jsonify({"ans": "error, try to check all params"})
        st_event = db_app.cons_repo.get_st_event_by_id(st_event_id)
        if st_event is None:
            jsonify({"ans": "there is no stateless event with id {}".format(st_event_id)})
        return jsonify({"ans": db_app.cons_repo.delete_stateless_events(st_event_id)})

    def post(self):
        error, ans = st_event_controller()
        if error:
            return jsonify(ans)
        return jsonify({"ans": db_app.cons_repo.add_stateless_events(ans[0], ans[1], ans[2], ans[3])})

    def get(self):
        args = parser.parse_args()
        try:
            st_event_id = int(args["st_event_id"])
        except TypeError:
            return jsonify({"ans": "all id must be integers"})
        st_event = db_app.cons_repo.get_st_event_by_id(st_event_id)
        if st_event is None:
            return jsonify({"ans": "there is no stateless event with id {}".format(st_event_id)})
        return jsonify({"ans": {"title": st_event.title, "contact": st_event.contact,
                                "description": st_event.description,
                                "date": ".".join(
                                    [str(st_event.date.day), str(st_event.date.month), str(st_event.date.year)]),
                                "customer": {"id": st_event.customer.id, "name": st_event.customer.name,
                                             "login": st_event.customer.login}}})


class StatelessEvents(Resource):
    def get(self):
        resp = []
        st_events = db_app.cons_repo.get_all_st_events()
        for st_event in st_events:
            resp.append({"title": st_event.title, "contact": st_event.contact,
                         "description": st_event.description,
                         "date": ".".join([str(st_event.date.day), str(st_event.date.month), str(st_event.date.year)]),
                         "customer": {"id": st_event.customer.id, "name": st_event.customer.name,
                                      "login": st_event.customer.login}})
        return jsonify(resp)
