from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, CourseModel, InstructorModel
from schema import TagSchema, TagAndCourseSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")

@blp.route("/instructor/<string:instructor_id>/tag")
class TagsOfInstructor(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, instructor_id):
        instructor = InstructorModel.query.get_or_404(instructor_id)
        return instructor.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, instructor_id):
        if(TagModel.query.filter(TagModel.instructor_id == instructor_id,
                                 TagModel.name == tag_data["name"]).first() ):
            abort(400, message="A tag with that name already exists for that instructor.")

        tag = TagModel(**tag_data, instructor_id=instructor_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )
        return tag


@blp.route("/course/<string:course_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, course_id, tag_id):
        course = CourseModel.query.get_or_404(course_id)
        tag = TagModel.query.get_or_404(tag_id)

        course.tags.append(tag)

        try:
            db.session.add(course)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndCourseSchema)
    def delete(self, course_id, tag_id):
        course = CourseModel.query.get_or_404(course_id)
        tag = TagModel.query.get_or_404(tag_id)

        course.tags.remove(tag)

        try:
            db.session.add(course)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Course removed from tag", "course": course, "tag": tag}


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no course is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more courses. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any courses, then try again.",
        )