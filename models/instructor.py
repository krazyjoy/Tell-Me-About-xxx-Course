from db import db


class InstructorModel(db.Model):
    __tablename__ = "instructors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    courses = db.relationship(
        "CourseModel",
        back_populates="instructor",
        lazy="dynamic",
        cascade="all, delete"
    )

    tags = db.relationship("TagModel", back_populates="instructor",lazy="dynamic")


