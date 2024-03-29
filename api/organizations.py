from flask import jsonify
from flask_restful import Resource, reqparse

from app.app import application

parser = reqparse.RequestParser()
parser.add_argument("name", required=True)
parser.add_argument("audience", required=False)


class Organization(Resource):
    def post(self):
        args = parser.parse_args()
        org_created_answer = application.org_repo.add_organization(org_name=args["name"])
        return jsonify({"ans": org_created_answer})

    def get(self):
        args = parser.parse_args()
        org, error = application.org_repo.get_org_by_name(name=args["name"])
        if error is None and org is not None:

            # events_this_org = application.event_repo.get_events_by_org_name(name=args["name"])
            count = 0
            for event in org.events:
                count += event.audience
            org.audience = count

            arr_events = []
            for event in org.events:
                arr_events.append({"id": event.id, "name": event.name})
            arr_customers = [{"id": customer.personality.id, "name": customer.personality.name} for customer
                             in application.cons_repo.get_customers_by_org(org=org)]

            return jsonify({"id": org.id, "name": org.name, "audience": org.audience,
                            "date": str(org.date.day) + "." + str(org.date.month) + "." + str(org.date.year),
                            "customers": arr_customers, "events": arr_events})

        elif error is None and org is None:
            return jsonify({"ans": "org with name {} not found".format(args["name"])})

        else:
            return jsonify({"ans": error})

    def delete(self):
        args = parser.parse_args()
        org, error = application.org_repo.get_org_by_name(name=args["name"])
        print(org, error)
        for event in org.events:
            application.cons_repo.del_curator(user_id=event.curator.id, event_id=event.id)
            application.cons_repo.del_customer(user_id=event.customer.id, event_id=event.id)
            application.event_repo.del_event(event.id)
        return jsonify({"ans": application.org_repo.del_org(org.id)})



class Organizations(Resource):
    def get(self):
        ans = {}
        for count, org in enumerate(application.org_repo.get_all_organizations()):
            ans[count+1] = [org.id, org.name]
        return jsonify(ans)
