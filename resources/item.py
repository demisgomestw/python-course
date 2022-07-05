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
            new_item = Item(name, data["price"], data["store_id"])
            new_item.save_to_db()
            return new_item.json(), 201
        except Exception:
            return {"message": f"An error occurred"}, 500

    def delete(self, name):
        item = Item.find_by_name(name)

        if item:
            item.delete_from_db()

        return {"message": "item deleted or does not exists"}, 204

    def put(self, name):
        data = request.get_json()
        item = Item.find_by_name(name)
        if item:
            item.price = data["price"]
            item.save_to_db()
            return {"item": item.json()}, 200

        new_item = Item(name, data["price"], data["store_id"])
        new_item.save_to_db()
        return {"item": new_item.json()}, 201


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in Item.query.all()]}
