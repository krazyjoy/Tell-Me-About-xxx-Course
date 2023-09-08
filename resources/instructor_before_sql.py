import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import instructors
from schema import InstructorSchema

blp = Blueprint("Instructor", __name__, description="course ratings")


@blp.route("/instructor/<string:instructor_id>")
class Instructor(MethodView):
    @blp.response(200, InstructorSchema)
    def get(self, instructor_id):
        try:
            return instructors[instructor_id]
        except KeyError:
            abort(404, message="instructor not found...")
    def delete(self, instructor_id):
        try:
            del instructors[instructor_id]
            return {"message": "instructor deleted"}
        except KeyError:
            abort(404, message="instructor not found")



@blp.route("/instructor")
class InstructorList(MethodView):
    @blp.response(200, InstructorSchema(many=True))
    def get(self):
        return {"instructors": list(instructors.values())}  # return json

    @blp.arguments(InstructorSchema)
    @blp.response(200, InstructorSchema)
    def post(self, instructor_data):
        for instructor in instructors.values():
            if (instructor_data["name"] in instructor["name"]):
                abort(400, message="instructor already exists...")
        instructor_id = uuid.uuid4().hex
        instructor = {**instructor_data, "id": instructor_id}
        instructors[instructor_id] = instructor
        return instructor, 201