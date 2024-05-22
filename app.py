from flask import Flask, request
from flask_smorest import abort
from db import items, stores
import uuid

app = Flask(__name__)


@app.get("/store") #http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message = 'Store not found.')

@app.post("/store")
def create_store():
    
    store_data = request.get_json()
    
    if ("name" not in store_data):
       abort(400, message = 'Bad request. Please ensure store name is there.')
       
    for store in stores.values():
        if store['name'] == store_data['name']:
            return abort(400, message = 'Store already exists.')
       
       
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message':'Store has been deleted.'}
    except KeyError:
        abort(404, message = 'Store not found.')
  
  
@app.get("/item")
def get_items():
    return {"items": list(items.values())}

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message = 'Item not found.')


@app.post("/item")
def create_item():
    item_data = request.get_json()
    
    if ("store_id" not in item_data or "price" not in item_data or "name" not in item_data):
       abort(400, message = 'Bad request. Please ensure all the values are there.')
    
    if item_data['store_id'] not in stores:
       abort(400, message = 'Store not found.')
       
    for item in items.values():
        if item['name'] == item_data['name'] and item['store_id'] == item_data['store_id']:
            return abort(400, message = 'Item already exists.')
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    
    return item, 201

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {'message':'item has been deleted.'}
    except KeyError:
        abort(404, message = 'Item not found.')

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    
    if ("price" not in item_data or "name" not in item_data):
        abort(400, message = 'Bad request. Please ensure all the values are there.')
    
    try:
        item = {**item_data, "id": item_id}
        items[item_id] = item
    except KeyError:
        abort(400, message = 'Item not found.')
        
    return item, 201