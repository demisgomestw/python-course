import sqlite3

from flask import request
from flask_restful import Resource


class UserResource(Resource):
    def post(self):
        data = request.get_json()
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users values (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"],))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
