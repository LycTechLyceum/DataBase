import os

from app.app import db_app
from api.curator import Curator
from api.curators import Curators
from api.customer import Customer
from api.customers import Customers
from api.event import Event
from api.events import Events
from api.leader import Leader
from api.leaders import Leaders
from api.organizations import Organization, Organizations
from api.position import Position
from api.positions import Positions
from api.practice import Practice
from api.practices import Practices
from api.proger import Proger
from api.progers import Progers
from api.user import User
from api.users import Users
from api.visitor import Visitor
from api.visitors import Visitors
from api.visitor_practices import VisitorPractice
from api.visitors_practices import VisitorsPractices
from api.check_password import Checker
from api.check_token import CheckerToken
from api.user_by_login import UserData
from api.stateless_event import StatelessEvent, StatelessEvents


db_app.api.add_resource(Curator, "/api/curator")  # ok
db_app.api.add_resource(Curators, "/api/curators")  # ok
db_app.api.add_resource(Customer, "/api/customer")  # ok
db_app.api.add_resource(Customers, "/api/customers")  # ok
db_app.api.add_resource(Event, "/api/event")  # ok
db_app.api.add_resource(Events, "/api/events")  # ok
db_app.api.add_resource(Leader, "/api/leader")  # ok
db_app.api.add_resource(Leaders, "/api/leaders")  # ok
db_app.api.add_resource(Organization, "/api/organization")  # ok
db_app.api.add_resource(Organizations, "/api/organizations")  # ok
db_app.api.add_resource(Position, "/api/position")  # ok
db_app.api.add_resource(Positions, "/api/positions")  # ok
db_app.api.add_resource(Practice, "/api/practice")  # ok
db_app.api.add_resource(Practices, "/api/practices")  # ok
db_app.api.add_resource(Proger, "/api/proger")  # ok
db_app.api.add_resource(Progers, "/api/progers")  # ok
db_app.api.add_resource(User, "/api/user")  # ok
db_app.api.add_resource(Users, "/api/users")  # ok
db_app.api.add_resource(Visitor, "/api/visitor")  # ok
db_app.api.add_resource(Visitors, "/api/visitors")  # ok
db_app.api.add_resource(VisitorPractice, "/api/visitor-practice")  # ok
db_app.api.add_resource(VisitorsPractices, "/api/visitors-practices")  # ok
db_app.api.add_resource(Checker, "/api/check-password")
db_app.api.add_resource(CheckerToken, "/api/check-token")
db_app.api.add_resource(UserData, "/api/user-data")
db_app.api.add_resource(StatelessEvent, "/api/stateless-event")
db_app.api.add_resource(StatelessEvents, "/api/stateless-events")


#  TODO: добавть delete всяких вещей

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db_app.run(host='0.0.0.0', port=port)
