from flask_restful import Resource, reqparse
from app.app import db_app


# parser = reqparse.RequestParser()
# parser.add_argument("name", required=True)
# parser.add_argument("surname", required=True)
# parser.add_argument("grade", required=True)
# parser.add_argument("login", required=True)
# parser.add_argument("created_date", required=False)
# parser.add_argument("id_", required=False)


class Users(Resource):
    def get(self):
        response = {}
        for persona in db_app.user_repo.get_all_users():
            response[persona.id] = {"name": persona.name, "surname": persona.surname}
        return response

# api/add_user (-> параметры пользователя)

# https://lyctech/api/all_users
