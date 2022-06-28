import sqlite3

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class Item(Resource):
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return {"item": {"name": item[0], "item": item[1]}}, 200

        return {"item": None}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * from items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"name": name, "price": row[1]}

        return None

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items values (?, ?)"
        cursor.execute(query, (item["name"], item["price"],))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE items set price=? where name=?"
        cursor.execute(query, (item["price"], item["name"],))
        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        data = request.get_json()
        item = self.find_by_name(name)
        if item:
            return {"message": f"This name ({name}) already exists"}, 400

        try:
            Item.insert({"name": name, "price": data["price"]})
            return item, 201
        except Exception:
            return {"message": f"An error occurred"}, 500

    @classmethod
    def delete(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE from items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message": "item deleted or does not exists"}

    def put(self, name):
        data = request.get_json()
        item = Item.find_by_name(name)
        if item:
            Item.update(item)
            return {"item": item}

        Item.insert({"name": name, "price": data["price"]})
        return {"item": item}, 201


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * from items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()
        return {"items": items}
