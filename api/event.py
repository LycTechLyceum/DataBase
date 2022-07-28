from flask import jsonify
from flask_restful import Resource, reqparse
from app.app import db_app

parser = reqparse.RequestParser()
parser.add_argument("event_name", required=False)
parser.add_argument("login_cus", required=False)
parser.add_argument("login_cur", required=False)
parser.add_argument("org_name", required=False)
parser.add_argument("id", required=False)


class Event(Resource):

    def post(self):
        args = parser.parse_args()
        name = args["event_name"]
        login_cur = args["login_cur"]
        login_cus = args["login_cus"]
        org_name = args["org_name"]
        cus = db_app.user_repo.get_persona_by_login(login=login_cus)
        cur = db_app.user_repo.get_persona_by_login(login=login_cur)
        org, error = db_app.org_repo.get_org_by_name(name=org_name)

        if cus is None:
            return jsonify({"error": "there is no user with login {}".format(login_cus)})
        elif cur is None:
            return jsonify({"error": "there is no user with login {}".format(login_cur)})
        elif org is None:
            return jsonify({"error": "there is no organization with name {}".format(org_name)})

        add_event_callback = db_app.event_repo.add_event(
            event_name=name,
            per_cus=cus,
            per_cur=cur,
            org=org
        )
        return jsonify({"ans": add_event_callback})

    def get(self):
        try:
            id = int(parser.parse_args()["id"])
            if id <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id event must be integer"})
        event = db_app.event_repo.get_event_by_id(id=id)
        if event is not None:
            progers = db_app.cons_repo.get_progers_by_event_id(id=id)
            if type(progers) == str:
                return jsonify({"ans":  progers})

            visitors = db_app.cons_repo.get_visitors_by_event_id(id=id)
            if type(visitors) == str:
                return {"ans": visitors}

            else:
                print(progers, visitors)
                devs = []
                for proger in progers:
                    devs.append({"id": proger.personality.id, "name": proger.personality.name})

                visits = []
                for visitor in visitors:
                    visits.append({"id": visitor.personality.id, "name": visitor.personality.name})
                date = str(event.date.day) + "." + str(event.date.month) + "." + str(event.date.year)
                response = {"id": event.id, "name": event.name, "date": date,
                            "curator": {"id": event.curator.id, "name": event.curator.name},
                            "customer": {"id": event.customer.id, "name": event.customer.name},
                            "organization": {"id": event.organization.id, "name": event.organization.name},
                            "progers": devs, "visitors": visits}
                return jsonify(response)

    def delete(self):
        try:
            id = int(parser.parse_args()["id"])
            if id <= 0:
                raise TypeError
        except TypeError:
            return jsonify({"ans": "id event must be integer"})
        event = db_app.event_repo.get_event_by_id(id=id)
        if not event:
            return jsonify({"ans": "there is no event with id {}".format(id)})
        else:
            db_app.cons_repo.del_curator(user_id=event.curator.id, event_id=id)
            db_app.cons_repo.del_customer(user_id=event.customer.id, event_id=id)
            return jsonify({"ans": db_app.event_repo.del_event(id)})

