from flask import jsonify
from flask_restful import Resource
from app.app import db_app


class Customers(Resource):
    def get(self):
        all_customers = db_app.cons_repo.get_all_customers()
        response = {}
        for customer in all_customers:
            if customer.personality.id not in response.keys():
                response[customer.personality.id] = {"id": customer.personality.id, "name": customer.personality.name,
                                                     "surname": customer.personality.surname,
                                                     "events": [{"id": customer.event.id, "name": customer.event.name}]}
            else:
                response[customer.personality.id]["events"].append({"id": customer.event.id,
                                                                    "name": customer.event.name})
        return jsonify(response)
