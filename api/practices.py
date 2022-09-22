from flask import jsonify
from flask_restful import Resource
from app.app import application


class Practices(Resource):
    def get(self):
        response = {}
        for practice in application.cons_repo.get_all_practices():
            response[practice.id] = {"name": practice.name,
                                     "date": f"{practice.date.day}.{practice.date.month}.{practice.date.year}",
                                     "id": practice.id}
        return jsonify(response)
