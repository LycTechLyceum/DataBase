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


db_app.api.add_resource(Curator, "/api/post-curator")
db_app.api.add_resource(Curators, "/api/get-curators")
db_app.api.add_resource(Customer, "/api/post-customer")
db_app.api.add_resource(Customers, "/api/get-customers")
db_app.api.add_resource(Event, "/api/post-event")
db_app.api.add_resource(Events, "/api/get-events")
db_app.api.add_resource(Leader, "/api/post-leader")
db_app.api.add_resource(Leaders, "/api/get-leaders")
db_app.api.add_resource(Organization, "/api/post-organization")
db_app.api.add_resource(Organizations, "/api/get-organizations")
db_app.api.add_resource(Position, "/api/position")
db_app.api.add_resource(Positions, "/api/get-positions")
db_app.api.add_resource(Practice, "/api/post-practice")
db_app.api.add_resource(Practices, "/api/get-practices")
db_app.api.add_resource(Proger, "/api/post-proger")
db_app.api.add_resource(Progers, "/api/get-progers")
db_app.api.add_resource(User, "/api/post-user")
db_app.api.add_resource(Users, "/api/get-users")
db_app.api.add_resource(Visitor, "/api/post-visitor")
db_app.api.add_resource(Visitors, "/api/get-visitors")
db_app.api.add_resource(VisitorPractice, "/api/post-visitor-practice")
db_app.api.add_resource(VisitorsPractices, "/api/get-visitors-practices")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db_app.run(host='0.0.0.0', port=port)
