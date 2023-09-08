from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey("instructors.id"), nullable=False)

    instructor = db.relationship("InstructorModel", back_populates="tags")
    courses = db.relationship("CourseModel", back_populates="tags", secondary="course_tags")


