from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from item import Item, ItemList
from user import User, UserRegister

app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if User.find_by_username(data["username"]):
        return {"access_token": create_access_token(identity=data["username"])}

    return jsonify({"message": "username/password are incorrect"}, 401)


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/users")

if __name__ == "__main__":
    app.run()
