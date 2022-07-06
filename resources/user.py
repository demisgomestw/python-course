from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from models.user import User


class UserResource(Resource):
    def post(self):
        data = request.get_json()
        user = User(data["username"], data["password"])
        user.save_to_db()

        return {"message": "User created successfully"}, 201

    def delete(self, _id):
        user = User.find_by_id(_id)
        if user:
            user.delete_from_db()

        return {"message": "User deleted or does not exist"}, 204

    def get(self, _id):
        user = User.find_by_id(_id)
        if user:
            return user.json()

        return {"message": "User does not exist"}, 404


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.find_by_username(data["username"])
        if user and data["password"] == user.password:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        return {"message": "username/password are incorrect"}, 401
