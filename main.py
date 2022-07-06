from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.item import ItemResource, ItemList
from resources.store import StoreResource, StoreList
from resources.token import TokenResource
from resources.user import UserResource, UserLogin

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

api.add_resource(ItemResource, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserResource, "/users")
api.add_resource(StoreResource, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenResource, "/refresh")

if __name__ == "__main__":
    db.init_app(app)
    app.run()
