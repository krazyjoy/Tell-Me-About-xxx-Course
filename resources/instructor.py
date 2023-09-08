import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from schema import InstructorSchema
from models import InstructorModel
blp = Blueprint("Instructor", __name__, description="course ratings")


@blp.route("/instructor/<string:instructor_id>")
class Instructor(MethodView):
    @blp.response(200, InstructorSchema)
    def get(self, instructor_id):
        instructor = InstructorModel.query.get_or_404(instructor_id)
        return instructor

    def delete(self, instructor_id):
        instructor = InstructorModel.query.get_or_404(instructor_id)
        db.session.delete(instructor)
        db.session.commit()
        return {"messsage":"Instructor deleted"}, 200


@blp.route("/instructor")
class InstructorList(MethodView):
    @blp.response(200, InstructorSchema(many=True))
    def get(self):
        return InstructorModel.query.all()

    @blp.arguments(InstructorSchema)
    @blp.response(200, InstructorSchema)
    def post(self, instructor_data):
        instructor = InstructorModel(**instructor_data)
        try:
            db.session.add(instructor)
            db.session.commit()
        except IntegrityError: # instructor name unique=True
            abort(400, message="instructor already exists...")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the instructor")
        return instructor


