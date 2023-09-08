from db import db


class CourseModel(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    department = db.Column(db.String(30), unique=False, nullable=False)
    difficulty = db.Column(db.Integer, unique=False, nullable=False)
    loading = db.Column(db.Integer, unique=False, nullable=False)
    usefulness = db.Column(db.Integer, unique=False, nullable=False)
    instructor_id = db.Column(db.Integer,
                              db.ForeignKey("instructors.id"),

                              unique=False, nullable=False)

    # one-to-many relationship
    instructor = db.relationship("InstructorModel", back_populates="courses")
    tags = db.relationship("TagModel", back_populates="courses", secondary="course_tags")







