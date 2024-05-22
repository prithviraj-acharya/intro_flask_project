import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on Item")

# http://127.0.0.1:5000/


@blp.route("/item/<string:item_id>")
class Store(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "item has been deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):

        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Please ensure all the values are there.")

        try:
            item = {**item_data, "id": item_id}
            items[item_id] = item
        except KeyError:
            abort(400, message="Item not found.")

        return item


@blp.route("/item")
class Store(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return {"items": list(items.values())} -- This is normal list return
        return items.values()  # This is for the ItemSchema(many=True)

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):

        if item_data["store_id"] not in stores:
            abort(400, message="Store not found.")

        for item in items.values():
            if (
                item["name"] == item_data["name"]
                and item["store_id"] == item_data["store_id"]
            ):
                return abort(400, message="Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item
