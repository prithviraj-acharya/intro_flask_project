from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Test Store",
        "items": [
            {
                'name': 'Chair',
                'price': 15.99
            },
            {
                'name': 'Table',
                'price': 10.99
            }
        ]
    }
]

@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if (store['name'] == name):
            new_items = {'name': request_data['name'], 'price': request_data['price']}    
            store['items'].append(new_items)
            return new_items, 201
    return {'message':'No stores found'}, 404


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if (store['name'] == name):
            return store
    return {'message':'No stores found'}, 404


@app.get("/store/<string:name>/items")
def get_item_in_store(name):
    for store in stores:
        if (store['name'] == name):
            return {'items': store['items'], "Message":"Items found successfullu"}
    return {'message' : 'No stores found'}, 404