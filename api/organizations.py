from flask import jsonify
from flask_restful import Resource, reqparse

from app.app import db_app

# parser = reqparse.RequestParser()
# parser.add_argument("id", required=False)
# parser.add_argument("name", required=True)
# parser.add_argument("audience", required=False)


class Organization(Resource):
    def post(self, name):
        # args = parser.parse_args()
        # org_created_answer = db_app.org_repo.add_organization(org_name=args["name"])
        org_created_answer = db_app.org_repo.add_organization(org_name=name)
        # return jsonify({"ans": org_created_answer})
        return {"ans": org_created_answer}

    def get(self, name):
        # args = parser.parse_args()
        # org, error = db_app.org_repo.find_org_by_name(args["name"])
        org, error = db_app.org_repo.get_org_by_name(name)
        if error is None and org is not None:

            events_this_org = db_app.event_repo.get_events_by_org_name(name=name)
            count = 0
            for event in events_this_org:
                count += event.audience
            org.audience = count

            arr_events = []
            for event in org.events:
                arr_events.append({"id": event.id, "name": event.name})
            arr_customers = [{"id": customer.personality.id, "namme": customer.personality.name} for customer
                             in db_app.cons_repo.get_customers_by_org(org=org)]

            # return jsonify({"id": org.id, "name": org.name, "audience": org.audience, "date": org.date,
            #                     "customers": arr_customers, "events": arr_events})
            return {"id": org.id, "name": org.name, "audience": org.audience,
                    "date": str(org.date.day) + "." + str(org.date.month) + "." + str(org.date.year),
                    "customers": arr_customers, "events": arr_events}

        elif error is None and org is None:
            # return "org with name {} not found".format(args["name"])
            return {"ans": "org with name {} not found".format(name)}

        else:
            # return jsonify({"ans": error})
            return {"ans": error}


class Organizations(Resource):
    def get(self):
        ans = {}
        for count, org in enumerate(db_app.org_repo.get_all_organizations()):
            ans[count+1] = org.name
        # return jsonify(ans)
        return ans
