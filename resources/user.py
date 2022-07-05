from flask import request
from flask_restful import Resource

from models.user import User


class UserResource(Resource):
    def post(self):
        data = request.get_json()
        user = User(data["username"], data["password"])
        user.save_to_db()

        return {"message": "User created successfully"}, 201
