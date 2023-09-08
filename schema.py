from marshmallow import Schema, fields

class PlainInstructorSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()

class PlainCourseSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    department = fields.Str(required=True)
    difficulty = fields.Int(required=True)
    loading = fields.Int(required=True)
    usefulness = fields.Int(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class InstructorSchema(PlainInstructorSchema):
    courses = fields.List(fields.Nested(PlainCourseSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class CourseSchema(PlainCourseSchema):
    instructor_id = fields.Str(required=True, load_only=True)
    # nested schema
    instructor = fields.Nested(PlainInstructorSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class CourseUpdateSchema(Schema):
    name = fields.Str()
    department = fields.Str()
    difficulty = fields.Int()
    loading = fields.Int()
    usefulness = fields.Int()

class TagSchema(PlainTagSchema):
    instructor_id = fields.Int(load_only=True)
    instructor = fields.Nested(PlainInstructorSchema(), dump_only=True)
    courses = fields.List(fields.Nested(PlainCourseSchema()), dump_only=True)

class TagAndCourseSchema(Schema):
    message=fields.Str()
    course = fields.Nested(CourseSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)

