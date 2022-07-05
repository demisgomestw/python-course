from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.store import Store


class StoreResource(Resource):
    def get(self, name):
        store = Store.find_by_name(name)

        if store:
            return store.json(), 200

        return {"store": None}, 404

    @jwt_required()
    def post(self, name):
        store = Store.find_by_name(name)
        if store:
            return {"message": f"This name ({name}) already exists"}, 400

        try:
            new_store = Store(name)
            new_store.save_to_db()
            return new_store.json(), 201
        except Exception as e:
            print(e)
            return {"message": f"An error occurred"}, 500

    @jwt_required()
    def delete(self, name):
        store = Store.find_by_name(name)

        if store:
            store.delete_from_db()

        return {"message": "Store deleted or does not exists"}, 204


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in Store.query.all()]}
