import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CourseModel
from schema import CourseSchema,CourseUpdateSchema

blp = Blueprint("Course", __name__, description="course ratings")


@blp.route("/course/<string:course_id>")
class Course(MethodView):

    @blp.response(200, CourseSchema)
    def get(self, course_id):
        course = CourseModel.query.get_or_404(course_id)
        return course


    def delete(self, course_id):

        course = CourseModel.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {"message": "Course deleted"}


    @blp.arguments(CourseUpdateSchema)
    @blp.response(200, CourseSchema)
    def put(self, course_data, course_id):
        course = CourseModel.query.get_or_404(course_id)
        if course:
            course.name = course_data["name"]
            course.department = course_data["department"]
            course.difficulty = course_data["difficulty"]
            course.loading = course_data["loading"]
            course.usefulness = course_data["usefulness"]
        else:
            course = CourseModel(id = course_id, **course_data)
        db.session.add(course)
        db.session.commit()
        return course


@blp.route("/course")
class CourseList(MethodView):

    @blp.response(200, CourseSchema(many=True))
    def get(self):
        return CourseModel.query.all() # return as a list

    @blp.arguments(CourseSchema)
    @blp.response(201, CourseSchema)
    def post(self, course_data):
        course = CourseModel(**course_data)
        try:
            db.session.add(course)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the course")

        return course