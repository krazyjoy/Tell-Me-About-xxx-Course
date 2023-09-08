## docker images and containers
- build a docker image:
    ```
    docker build -t rest-apis-flask-python . 
    ```

- verify existence of image on docker desktop
  ```
  Images: rest-apis-flask-python
  ```
  - click on the `>` button to run the image
  - click `more options` to discover the optional settings <br>
    for example: we have `port number 5000` exposed in the image <br>
    if we type in `Ports: 5005` , app will be directed using port `5005` <br>
    say we use GET `http://127.0.0.1:5000/store` in insomnia it wouldn't work <br>
    instead we have to change the url to `http://127.0.0.1:5005/store`
  - note that we **do not** need to run `flask run` on pycharm or your ide <br><br>

- images and containers
  - containers have predefined storage, and it will maintain everything inside unless you `delete` the container <br>
  - you can create **any number of new containers** using the image `rest-apis-flask-python` <br><br>

- run docker image via command line
  - `docker run -p 5005:5000 -t rest-apis-flask-python`
    - `-p`: port forwarding
    - `-t`: tag name <br><br>
  - **YOU HAVE TO TERMINATE (NOT DELETE) YOUR CONTAINER ON THE DOCKER DESKTOP IN ORDER TO USE THE SAME PORT** <br> <br>
    - `(venv) D:\Flask>docker run -p 5005:5000 -t rest-apis-flask-python
docker: Error response from daemon: driver failed programming external connectivity on endpoint intelligent_hertz (a1a42fe18abfae2cef88dc5e9a02b086dac8efb18209a0ec510f53082cd41924): Bind for 0.0.0.0:5005 failed: port is already allocated.
`   <br><br>

    - every time you use `docker run` it creates a new container
    - try to see the api on browser: 
      - it says `Running on http://127.0.0.1:5000` on terminal
      - but use `http://127.0.0.1:5005/store` <br><br>
    - if we need to run docker image in the background, so we can use the terminal, add `-d` for deamon
      - `docker run -d -p 5005:500 -t rest-apis-flask-python`

- check functions: 
  - GET `http://127.0.0.1:5005/store/tech shop`
    1. go to insomnia and use POST `/store/<string:store_name>` to create new store
        ```
        url: http://127.0.0.1:5005/store/tech shop
        {
          "name":"tech shop"
        }
        ```
    2. go to insomnia and use `POST /store/<string:store_name>/item` to create new items
       ```
       url: http://127.0.0.1:5005/store/tech shop/item
       {
         "name": "laptop",
         "price": 300
       }
       ```
     3. go to browser and use GET `http://127.0.0.1:5005/store/tech shop` to check if store exist
  
  
## Data Model Improvement
- install new libraries in python using `requirements.txt`
  ```
  flask
  flask-smorest
  python-dotenv 
  ```
- create `.flaskenv`, this includes the variables we want to use when we start up those libraries 
  ```
  FLASK_APP=app  # where we write our flask app (in app.py)
  FLASK_DEBUG=1 # allows to modify codes w/o restarting the program
  ```
- `python-dotenv` will satisfy the settings in `.flaskenv`
- run `flask run`
  - receive message: `There are .env or .flaskenv files present. Do "pip install python-dotenv" to use them.`
  - install everything: `pip install -r requirements.txt`, then run `flask run` again
  - if success should receive message:
    ``` 
     * Serving Flask app 'app'
     * Debug mode: on
     WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000

    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 109-144-346
    ```
  <br>

### Modify data structures
1. To better access items/stores by ID, rather than name (for query beneficiaries). <br>
Instead of using list for `stores` and `items`, we use dictionary (object) that contains `id` for each product and store

   - Before
     ```
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
     ```
   - after
     ```
     items = {
       1:{
           "name": "chair",
           "price": 17.99
       },
       2:{
           "name": "table",
           "price": 45.00
       }

     }
     ```
ex: `items[1]` to get the item with a key of `1`

2. Separate app functions from data
   - create a new file `db.py`
   - throw dictionaries to `db.py`
   - to use the data structures: import variables from file `from db import stores,items`

3. get_store()
    - pass in store_id using url
        `http://127.0.0.1:5005/store/<string:store_id>`
    - `stores` is now a dictionary, so we can access values with `stores[store_id]`
    - use `try, except` to avoid key error access
4. create_item()
    - `@app.post("/item")` because we are now using store id instead of store name
    - send json data from insomnia includes store id, item name, item price
    - use request.get_json() to generate item-data, then compare its store id with the existed store ids in dictionary (db.py)
5. get_all_items()
    - separate items from stores (do not have to iterate over all stores)
    - `return {"items":list(items.values())}` (we don't want to output store ids(items keys))

6. get_item()
    - retrieve a single item
    - `@app.get(/item/<string:item_id>)`
    - `return items[item_id]` 

## Test Around Using Identifiers
Since we are now funning using `flask run` the port number is `5000`

1. create new store:
    - POST /store CREATE NEW STORE `http://127.0.0.1:5000/store`
    
    ```
    (JSON)
    {
	    "name":"tech shop"
	
    }
    (result) 
    {
	    "id": "962122e972c34601bff9fd933a28b9d5",
	    "name": "tech shop"
    }
    ```
2. get specific store:
    - GET /store GET STORE 
    ```
    http://127.0.0.1:5000/store/eec567fb28354761b85793d02eaa9379
    ```
3. create new item
    - POST /item `http://127.0.0.1:5000/item`
    ```
     (JSON)
     {
       "name": "laptop",
       "price": 300,
       "store_id": "962122e972c34601bff9fd933a28b9d5"
     }
     
    (RESULT) generate a unique id for item
     {
	   "id": "75630ac011734f34bd7d9777740b49ab",
	   "name": "laptop",
	   "price": 300,
	   "store_id": "962122e972c34601bff9fd933a28b9d5"
    }
    ```
4. get_all_items()
   - `http://127.0.0.1:5000/item`
   ```
       {
       "items": [
           {
               "name": "chair",
               "price": 17.99
           },
           {
               "name": "table",
               "price": 45.0
           },
           {
               "id": "75630ac011734f34bd7d9777740b49ab",
               "name": "laptop",
               "price": 300,
               "store_id": "962122e972c34601bff9fd933a28b9d5"
		   }
	   ]
    }
   ```
   
6. get specific item
    - get_item() use `item id` to access product info
    <br>
    ```
     {
       "id": "75630ac011734f34bd7d9777740b49ab",
       "name": "laptop",
       "price": 300,
       "store_id": "962122e972c34601bff9fd933a28b9d5"
     }
    ```
## Abort
when there is error occurring while using requests, if we use `return {"message":"your error message}` <br>
it is not visible from outside the development space <br>

Therefore, I use `abort` in `flask-smorest` 

- `create_item()`: change error message to abort
  ```
  if item_data["store_id"] not in stores:
        return {"message":"Store not found"}, 404`
  ```
  - `abort(404, message=store not found)`


## Error Handling
`create_item()`
- If duplicate items exists in the same store, we should not allow same item to be generated again <br>
    - iterate over all `items.values()` since `items` has data type `dictionary` 
- If item data does not contain all the information, item cannot be created
  - `price, store_id, name` need to exist in `item_data`

<br>

`create_store()`
- If duplicate stores exists in `stores` it will cause confusions
    - iterate over all `stores.values()` to check if `store_data['name']` is the same
- `store_data` payload must contain `name`


## Update Endpoint names (insomnia)
1. create two folders (stores, and items)
2. rename requests from name to id
    ```
        Items>
            GET> /item GET ALL ITEMS
            GET> /item/<item_id> GET SPECIFIC ITEM
            POST> /item    CREATE NEW ITEM
        
        Stores>
            GET> /store GET ALL STORES
            GET> /store/<store_id> GET SPECIFIC STORE
            POST> /store CREATE NEW STORE
        
    ```
3. add updates and deletes
    ```
        Items>
            GET> /item GET ALL ITEMS
            GET> /item/<item_id> GET SPECIFIC ITEM
            POST> /item    CREATE NEW ITEM
            PUT> /item/<item_id> UPDATE ITEM
            DEL> /item/<item_id> DELETE ITEM
        Stores>
            GET> /store GET ALL STORES
            GET> /store/<store_id> GET SPECIFIC STORE
            POST> /store CREATE NEW STORE
            PUT> /store/<store_id>  UPDATE STORE
            DEL> /store/<store_id>  DELETE STORE
        
    ```
   
## Handle delete endpoint
`delete` is similar to `get` in that they both need to check if the current item id exist in dictionary <br>
- use `try, except` to manage key error exceptions
- use `del` for deletion
- test insomnia to see if delete endpoint receive `{
    "message": "Item deleted"
  }`
- test insomnia to see if get all items have removed the item just created

## Handle update endpoint
To update data we need to retrieve the json data from user.
 - `request.get_json()`

Check json payload contains necessary information
- `if "price" not in item_data or "name" not in item_data:`

Check if item exists in items
- `try, except` to handle `item_id` error case

