from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token

from db import db
from models.user import User
from resources.item import ItemResource, ItemList
from resources.store import StoreResource, StoreList
from resources.user import UserResource

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    retrieved_user = User.find_by_username(data["username"])
    if retrieved_user and data["password"] == retrieved_user.password:
        return {"access_token": create_access_token(identity=data["username"])}

    return jsonify({"message": "username/password are incorrect"}, 401)


api.add_resource(ItemResource, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserResource, "/users")
api.add_resource(StoreResource, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    db.init_app(app)
    app.run()
