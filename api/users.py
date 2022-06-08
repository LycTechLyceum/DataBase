from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument("name", required=True)
parser.add_argument("surname", required=True)
parser.add_argument("grade", required=True)
parser.add_argument("login", required=True)
parser.add_argument("created_date", required=False)
parser.add_argument("id_", required=False)


class User(Resource):
    def post(self):
        pass

# api/add_user (-> параметры пользователя)

 # https://lyctech/api/all_users