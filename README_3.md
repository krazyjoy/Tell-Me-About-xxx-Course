## Data Validation
We need to implement schemas to ensure our input data matches the format of our fields

-> Marshmellow (add marshmellow to requirements.txt)

- create a file name `schema.py`
- define fields and how they behave

  - `dump_only`: true: only return data
  - `required`: true: must have forward and return data
- instructor:
  - id: dump_only
  - name: required

`course.py` post course
- import schema
  - `from schema import CourseSchema`
    - replace the 'name', 'department', .... item checking to schema
      
           course_data = request.get_json()
           if ("department" not in course_data
                          or "name" not in course_data
                          or "difficulty" not in course_data
                          or "loading" not in course_data
                          or "usefulness" not in course_data
                          or "instructor_id" not in course_data
                  ):
          
          AFTER>
          @blp.arguments(CourseSchema)
          def post(self, course_data):
            # no need to validate input json (course_data) is the parameter after courseSchema validation
  
`course.py` update course
- import update schema
```
@blp.arguments(CourseUpdateSchema)
```
- replace validation check to checked data `course_data`
```
@blp.arguments(CourseUpdateSchema)
    def put(self, course_data, course_id):
        try:
            course = courses[course_id]
            course |= course_data
            return course
        except KeyError:
            abort(404, message="Course not found")
```

`instructor.py` post instructor

- replace data validation from schema
    ```
            if ("name" not in instructor_data):
                abort(400, message="Bad Request: Ensure 'name' is included in instructor data")
    ```
    after
    ```
      @blp.arguments(InstructorSchema)
      def post(self, instructor_data):
    ```
  
- Schema will also be updated on `http://127.0.0.1:5000/swagger-ui` at the bottom of the template


## Decorating Responses Using Marshmellow
Pass the data returning through schema like Filtering and Casting with Marshmellow

1. Define what to return for each status code
    ex: pass return from class course function get to Course Schema
    ```
    @blp.response(200, CourseSchema)
        def get(self, course_id):
            try:
                return courses[course_id]
            except KeyError:
                abort(404, message="Course not found...")
    
   ```
   ex: `id` in CourseSchema is `dump_only`, it will be returned to our schema, and `required` is included in both ends,
        so they will appear in our schema as well. <br><br>

2. apply to all has `return object` functions
    - put() in course class
      ```
      1. place @blp.response() under @blp.arguments() because responses comes the end of the function cycle
      2. place `courseSchema` instead of `CourseUpdateSchema` as return schema because we want to return `course` object after updating
      
      @blp.arguments(CourseUpdateSchema)
      @blp.response(200, CourseSchema)
      def put(self, course_data, course_id):
          try:
               course = courses[course_id]
               course |= course_data
               return course
      ```
      

## SQL Alchemy
- Benefits of using ORM:
- Multi-threading support
- Handling creating the tables and defining the rows
- Database migrations (with help of another library, Alembic)
- Like mentioned, it makes the code cleaner, simpler, and shorter

1. include the following packages to requirements.txt
```
sqlalchemy
flask-sqlalchemy
```

2. `pip install -r requirements.txt`

3. modifications happens on docker bc
   `COPY requirements.txt .
    RUN pip install -r requirements.txt    
   `
