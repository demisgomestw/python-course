import sqlite3

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.item import Item


class ItemResource(Resource):
    def get(self, name):
        item = Item.find_by_name(name)

        if item:
            return item.json(), 200

        return {"item": None}, 404

    @jwt_required()
    def post(self, name):
        data = request.get_json()
        item = Item.find_by_name(name)
        if item:
            return {"message": f"This name ({name}) already exists"}, 400

        try:
            new_item = Item(name, data["price"])
            new_item.insert()
            return new_item.json(), 201
        except Exception:
            return {"message": f"An error occurred"}, 500

    def delete(self, name):
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
            item.update()
            return {"item": item.json()}

        new_item = Item(name, data["price"])
        new_item.insert()
        return {"item": new_item.json()}, 201


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
