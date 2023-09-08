## RUN API ON DOCKER WHILE RELOADING CODE
Instead of running locally in development mode, we want to run on docker at all times
<br>

To do this, modify the dockerfile
```
FROM python:3.9
EXPOSE 5000
WORK_DIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run" "--host", "0.0.0.0"]

```

The reason why we want to do `COPY` twice is because if `requirements.txt` HAS NOT BEEN CHANGED,
then it will be cached on container, and we don't have to install packages again
<br>

command line:
`docker build -t flask-smorest-api .` (do not forget the `.`)
`docker run -d -p 5005:5000 -t flask-smorest-api`


### USE VOLUME TO AVOID REBUILDING IMAGE EVERYTIME WE CHANGE THE CODE

mac >
- `-dp 5000:5000` - same as before. Run in detached (background) mode and create a port mapping.
- `-w /app` - sets the container's present working directory where the command will run from.
- `-v "$(pwd):/app"` - bind mount (link) the host's present directory to the container's /app directory. Note: Docker requires absolute paths for binding mounts, so in this example we use pwd for printing the absolute path of the working directory instead of typing it manually.
flask-smorest-api - the image to use.

windows > <br>
`docker run -dp 5000:5000 -w /app -v "/d/Flask:/app" flask-smorest-api   `

- `-v "<project directory>"`, use `/d/` instead of `D:/`


-------------------------

1. verify if new code changes happens instantly on insomnia
   ```
    def get_all_items():
        return "HELLO WORLD"
   ```
   
## Insomnia Environment
(make sure your docker is running, if not `docker run -dp 5000:5000 -w /app -v "/d/Flask:/app" flask-smorest-api
`) <br>

To avoid url conflicts between various endpoints, we use insomnia to create a global url
<br>

- create json
   ```
    {
      "url":"http://127.0.0.1:5000" 
    }
   ```
- change all endpoints on insomnia to `{{url}}`+`/routes`

## Separate Store and Item Endpoints
Use Blueprints to segment different types of methods <br>
Then use MethodViews to do routing method
- create a folder `resources`
- create two files `store.py` and `item.py`

```
blp = Blueprint("stores",__name__, description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self):
        pass
    def delete(self):
        pass
```

- paste code from `app.py` (remember to pass in `store_id` argument)
```
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="store not found...")
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "store deleted"}
        except KeyError:
            abort(404, message="store not found")
```

## Change to Smorest

Finally, we have to import the Blueprints inside app.py, and register them with Flask-Smorest:
- include blueprints to `app.py`
```
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
```
Create our flask app and embedded with the flask_smorest framework by creating an Api object

```
from flask import Flask
from flask_smorest import Api
app = Flask(__name__)
app.config["..."] = ...
api = Api(app)

```
- add blueprints to api
```
api.register_api()

```

## swagger-ui

http://127.0.0.1:5000/swagger-ui


curl -X 'GET' \
  'http://127.0.0.1:5000/instructor/dc8e5ed4e9d64005b9ca854376fa5b8b' \
  -H 'accept: application/json'


Response: 200
{
  "id": "dc8e5ed4e9d64005b9ca854376fa5b8b",
  "name": "Lee Jian Lone"
}
