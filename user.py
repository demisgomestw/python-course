import sqlite3

from flask import request
from flask_restful import Resource


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.name = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
            user = User(*row)

        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = User(*row)

        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users values (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"],))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
