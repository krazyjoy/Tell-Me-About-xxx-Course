from db import db

class CourseTags(db.Model):
    __tablename__ = "course_tags"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))




