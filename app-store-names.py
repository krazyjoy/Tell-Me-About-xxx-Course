from flask import Flask, request

app = Flask(__name__)

"""
use store name to identify each store
"""
# temporary list
stores = [
    {
        "name": "My Store",
        "items":[
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

# endpoint
@app.get("/store") # http://127.0.0.1:5000/store
def get_stores(): # endpoint function
    return {"stores":stores}  # return json

# create a post request on insomnia but received 405 method not found, because we haven't created
# a method/endpoint to deal with this post request

@app.post("/store") # http://127.0.0.1:5000/store
def create_store():
    requested_data = request.get_json() # use flask-request
    new_data = {"name": requested_data["name"], "items": []}
    stores.append(new_data)
    return new_data, 201  # 201 stands for created

# we use database because python list only exists in memory not disk

"""
CREATE ITEM AND APPEND TO DICTIONARY
"""
@app.post("/store/<string:store_name>/item")  # use <type:param> format to pass variable through url (ex: http://127.0.0.1:5000/store/My Store/item)
def create_item(store_name):
    requested_data = request.get_json()
    new_item = {"name":requested_data["name"], "price":requested_data["price"]}
    for store in stores:
        if store["name"] == store_name: # look at the url after "string:"
            store["items"].append(new_item)
            return new_item, 201
    return {"message":"Store not found"}, 404

# insonmia get store to verify new item is added into list
# GET http://127.0.0.1:5000/store
# CRTL + '/'
# {
# 	"stores": [
# 		{
# 			"items": [
# 				{
# 					"name": "Chair",
# 					"price": 15.99
# 				},
# 				{
# 					"name": "table",
# 					"price": 17.99
# 				}
# 			],
# 			"name": "My Store"
# 		}
# 	]
# }

"""
GET SPECIFIC STORE / STORE ITEMS
"""
@app.get("/store/<string:store_name>")
def get_store(store_name):
    for store in stores:
        if store_name == store["name"]:
            return store

    return {"message":"Store not found"}, 404

@app.get("/store/<string:store_name>/item")
def get_item_in_store(store_name):
    for store in stores:
        if store_name == store["name"]:
            return {"items":store["items"]} # return an object for the future adding features

    return {"message":"Store not found"}, 404