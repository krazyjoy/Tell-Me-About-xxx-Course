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
    say we use GET `http://127.0.0.1:5000/course` in insomnia it wouldn't work <br>
    instead we have to change the url to `http://127.0.0.1:5005/course`
  - note that we **do not** need to run `flask run` on pycharm or your ide <br><br>

- images and containers
  - containers have predefined storage, and it will maintain everything inside unless you `delete` the container <br>
  - you can create **any number of new containers** using the image `rest-apis-flask-python` <br><br>

- run docker image via command line
  - `docker run -p 5005:5000 -t course-rating-rest-apis-flask
    - `-p`: port forwarding
    - `-t`: tag name <br><br>
  - **YOU HAVE TO TERMINATE (NOT DELETE) YOUR CONTAINER ON THE DOCKER DESKTOP IN ORDER TO USE THE SAME PORT** <br> <br>
    - `(venv) D:\Flask>docker run -p 5005:5000 -t course-rating-rest-apis-flask
docker: Error response from daemon: driver failed programming external connectivity on endpoint intelligent_hertz (a1a42fe18abfae2cef88dc5e9a02b086dac8efb18209a0ec510f53082cd41924): Bind for 0.0.0.0:5005 failed: port is already allocated.
`   <br><br>

    - every time you use `docker run` it creates a new container
    - try to see the api on browser: 
      - it says `Running on http://127.0.0.1:5000` on terminal
      
    - if we need to run docker image in the background, so we can use the terminal, add `-d` for deamon
      - `docker run -d -p 5005:500 -t rest-apis-flask-python`

- check functions: 
  - GET `http://127.0.0.1:5005/course`
    1. go to insomnia and use POST `/course/` to create new user
        ```
        url: http://127.0.0.1:5005/course
        {
            "department":"CSE",
            "name":"Discrete Mathematics",
            "difficulty": 2,
            "loading": 2,
            "usefulness": 4,
            "instructor_id": "1"
        }
        ```
       2. go to insomnia and use `POST /course/<course_id>/tag/<tag_id>` to create new items
          ```
          url: http://127.0.0.1:5005//course/<course_id>/tag/<tag_id>
          
          ```
       
  
  
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
     courses = [
         {
             "name": "Embedded System",
             "department": "CSE",
             "difficulty": 5,
             "loading": 5,
             "usefulness": 4
             "tags": [],
             "instructor": {
             
			    "name": "Lee Jian Lone"
		     }
         },
        {
            "name": "Discrete Mathematics",
            "department": "CSE",
		    "difficulty": 2,
		    "usefulness": 4,
            "loading": 2,
            "tags": [],
		    "instructor": {
			    
			    "name": "Lee Jian Lone"
		    },
	    }
     ]
     ```
   - after
     ```
     courses = [
         {
             "id": "1",
             "name": "Embedded System",
             "department": "CSE",
             "difficulty": 5,
             "loading": 5,
             "usefulness": 4
             "tags": [],
             "instructor": {
                "id": "1",
			    "name": "Lee Jian Lone"
		     }
         },
        {
            "id": "2",
            "name": "Discrete Mathematics",
            "department": "CSE",
		    "difficulty": 2,
		    "usefulness": 4,
            "loading": 2,
            "tags": [],
		    "instructor": {
			    "id": "1",
			    "name": "Lee Jian Lone"
		    },
	    }
     ]
     ```
ex: `instructors[1]` to get the instructor with a key of `1`

2. Separate app functions from data
   - create a new file `db.py`
   - throw dictionaries to `db.py`
   - to use the data structures: import variables from file `from db import courses, instructors`

3. get_course()
    - pass in store_id using url
        `http://127.0.0.1:5005/course/<string:course_id>`
    - `course` is now a dictionary, so we can access values with `course[course_id]`
    - use `try, except` to avoid key error access
4. create_course()
    - `@app.post("/course")` because we are now using course id instead of course name
    - send json data from insomnia includes `course name`, `department`, `difficulty`, `loading`, `usefulness`, `instructor id`
    - use request.get_json() to generate item-data, then compare its course id with the existed course ids in dictionary (db.py)
5. get_all_courses()
    -  (do not have to iterate over all courses)
    - `return {"items":list(items.values())}` (we don't want to output store ids(items keys))

6. get_instructor()
    - retrieve a single item
    - `@app.get(/instructor/<string:instructor_id>)`
    - `return instructor[instructor_id]` 

## Test Around Using Identifiers
Since we are now running using `flask run` the port number is `5000`

1. create new course:
    - POST /store CREATE NEW COURSE `http://127.0.0.1:5000/course`
    
    ```
    (JSON)
    {
        "department":"CSE",
        "name":"Discrete Mathematics",
        "difficulty": 2,
        "loading": 2,
        "usefulness": 4,
        "instructor_id": "1"
    }
    (result) 
    {
        "department": "CSE",
        "difficulty": 2,
        "id": "2",
        "instructor": {
            "id": "1",
            "name": "Lee Jian Lone"
        },
        "loading": 2,
        "name": "Discrete Mathematics",
        "usefulness": 4
    }
    ```
   2. get specific store:
       - GET /course GET COURSE
       ```
       http://127.0.0.1:5000/course/1
        
       RETURN
        {
            "department": "CSE",
            "difficulty": 5,
            "id": "1",
            "instructor": {
                "id": "1",
                "name": "Lee Jian Lone"
            },
            "loading": 5,
            "name": "Embedded System",
            "tags": [],
            "usefulness": 4
        }
   
   
    ```
   3. create new instructor
       - POST /item `http://127.0.0.1:5000/instructor`
       ```
        (JSON)
        {
            "name":"Fredrick Louis"  
        }
     
       (RESULT) generate a unique id for instructor
        {
             "courses": [],
             "id": "2",
             "name": "Fredrick Louis",
             "tags": []
        }
       ```
      4. get_all_courses()
         - `http://127.0.0.1:5000/courses`
         ```
        [
	        {
		        "department": "CSE",
		        "difficulty": 5,
		        "id": "1",
		        "instructor": {
			        "id": "1",
			        "name": "Lee Jian Lone"
		        },
		        "loading": 5,
		        "name": "Embedded System",
		        "tags": [],
		        "usefulness": 4
	        },
	        {
		        "department": "CSE",
		        "difficulty": 2,
		        "id": "2",
		        "instructor": {
			        "id": "1",
			        "name": "Lee Jian Lone"
		    },
		        "loading": 2,
		        "name": "Discrete Mathematics",
		        "tags": [],
                "usefulness": 4
	        }
        ]
      ```
   
   6. get all instructor
       - get_instructors()
       <br>
       ```
        [
            {
                "courses": [
                {
                   "department": "CSE",
                   "difficulty": 5,
                   "id": "1",
                   "loading": 5,
                   "name": "Embedded System",
                   "usefulness": 4
               },
               {
                   "department": "CSE",
                   "difficulty": 2,
                   "id": "2",
                   "loading": 2,
                   "name": "Discrete Mathematics",
                   "usefulness": 4
               }
           ],
               "id": "1",
               "name": "Lee Jian Lone",
               "tags": [
                 {
                   "id": 1,
                   "name": "interesting"
                 }
           ]
       },
           {
               "courses": [],
               "id": "2",
               "name": "Fredrick Louis",
               "tags": []
           }
       ]
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
        Instructor>
            GET> /instructor GET ALL INSTRUCTORS
            GET> /instructor/<instructor_id> GET SPECIFIC INSTRUCTOR
            POST> /instructor    CREATE NEW INSTRUCTOR
            PUT> /instructor/<instructor_id> UPDATE INSTRUCTOR
            DEL> /instructor/<instructor_id> DELETE INSTRUCTOR
        Course>
            GET> /course GET ALL COURSES
            GET> /course/<course_id> GET SPECIFIC COURSE
            POST> /course CREATE NEW COURSE
            PUT> /course/<course_id>  UPDATE COURSE
            DEL> /course/<course_id>  DELETE COURSE
        
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

