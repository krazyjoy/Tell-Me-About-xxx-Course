import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import courses, instructors
from schema import CourseSchema,CourseUpdateSchema

blp = Blueprint("Course", __name__, description="course ratings")


@blp.route("/course/<string:course_id>")
class Course(MethodView):
    @blp.response(200, CourseSchema)
    def get(self, course_id):
        try:
            return courses[course_id]
        except KeyError:
            abort(404, message="Course not found...")

    def delete(self, course_id):
        try:
            del courses[course_id]
            return {"message": "Course deleted"}
        except KeyError:
            abort(404, message="Course not found")

    @blp.arguments(CourseUpdateSchema)
    @blp.response(200, CourseSchema)
    def put(self, course_data, course_id):
        try:
            course = courses[course_id]
            course |= course_data
            return course
        except KeyError:
            abort(404, message="Course not found")

@blp.route("/course")
class CourseList(MethodView):
    @blp.response(200, CourseSchema(many=True))
    def get(self):
        return courses.values()  # return as a list

    @blp.arguments(CourseSchema)
    @blp.response(201, CourseSchema)
    def post(self, course_data):
            # abort(400, message="Bad Request. Ensure 'department', 'name', 'difficulty', 'loading', 'usefulness', 'instructor' are included in the course data...")

        # no duplicated course taught by the same instructor
        for course in courses.values():
            if(course_data["name"] == course
                and course_data["instructor_id"] == course["instructor_id"]
            ):
                abort(400, message="Course already exists")

        course_id = uuid.uuid4().hex
        course = {**course_data, "id":course_id}
        courses[course_id] = course
        return course, 201