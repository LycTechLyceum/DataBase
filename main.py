import os

from app.app import application
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


application.api.add_resource(Curator, "/api/curator")  # ok
application.api.add_resource(Curators, "/api/curators")  # ok
application.api.add_resource(Customer, "/api/customer")  # ok
application.api.add_resource(Customers, "/api/customers")  # ok
application.api.add_resource(Event, "/api/event")  # ok
application.api.add_resource(Events, "/api/events")  # ok
application.api.add_resource(Leader, "/api/leader")  # ok
application.api.add_resource(Leaders, "/api/leaders")  # ok
application.api.add_resource(Organization, "/api/organization")  # ok
application.api.add_resource(Organizations, "/api/organizations")  # ok
application.api.add_resource(Position, "/api/position")  # ok
application.api.add_resource(Positions, "/api/positions")  # ok
application.api.add_resource(Practice, "/api/practice")  # ok
application.api.add_resource(Practices, "/api/practices")  # ok
application.api.add_resource(Proger, "/api/proger")  # ok
application.api.add_resource(Progers, "/api/progers")  # ok
application.api.add_resource(User, "/api/user")  # ok
application.api.add_resource(Users, "/api/users")  # ok
application.api.add_resource(Visitor, "/api/visitor")  # ok
application.api.add_resource(Visitors, "/api/visitors")  # ok
application.api.add_resource(VisitorPractice, "/api/visitor-practice")  # ok
application.api.add_resource(VisitorsPractices, "/api/visitors-practices")  # ok
application.api.add_resource(Checker, "/api/check-password")
application.api.add_resource(CheckerToken, "/api/check-token")
application.api.add_resource(UserData, "/api/user-data")
application.api.add_resource(StatelessEvent, "/api/stateless-event")
application.api.add_resource(StatelessEvents, "/api/stateless-events")


#  TODO: добавть delete всяких вещей

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)
