from flask import jsonify
from flask_restful import Resource
from app.app import db_app


class Event(Resource):

    def post(self, name, login_cus, login_cur, org_name):
        cus = db_app.user_repo.get_persona_by_login(login=login_cus)
        cur = db_app.user_repo.get_persona_by_login(login=login_cur)
        org, error = db_app.org_repo.get_org_by_name(name=org_name)

        if cus is None:
            # return jsonify({"error": "there is no user with login {}".format(login_cus)})
            return {"ans": "there is no user with login {}".format(login_cus)}
        elif cur is None:
            # return jsonify({"error": "there is no user with login {}".format(login_cur)})
            return {"ans": "there is no user with login {}".format(login_cur)}
        elif org is None:
            # return jsonify({"error": "there is no organization with name {}".format(org_name)})
            return {"ans": "there is no organization with name {}".format(org_name)}

        add_event_callback = db_app.event_repo.add_event(
            event_name=name,
            per_cus=cus,
            per_cur=cur,
            org=org
        )
        # return jsonify({"ans": add_event_callback})
        return {"ans": add_event_callback}

    def get(self, id):
        event = db_app.event_repo.get_event_by_id(id=id)
        if event is not None:
            progers = db_app.cons_repo.get_progers_by_event_id(id=id)
            if type(progers) == str:
                return {"ans":  progers}

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
                return response


