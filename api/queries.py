from ariadne import convert_kwargs_to_snake_case
from sqlalchemy import or_
from api.models import Student


def read_students_resolver(obj, info, limit=10, offset=0, specialization=None, degree=None, semester=None):
    try:
        query = Student.query
        if specialization:
            query = query.filter(or_(Student.specialization.in_(specialization), Student.specialization is None))
        if degree:
            query = query.filter(or_(Student.degree.in_(degree), Student.degree is None))
        if semester:
            query = query.filter(or_(Student.semester.in_(semester), Student.semester is None))
        students = [student.to_dict() for student in query.slice(offset, offset + limit).all()]
        total_count = query.count()
        current_page = int(offset / limit) + 1
        payload = {
            "success": True,
            "students": students,
            "total_count": total_count,
            "page": current_page
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def read_student_resolver(obj, info, id):
    try:
        student = Student.query.get(id)
        payload = {
            "success": True,
            "student": student.to_dict()
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Error / read_student_resolver: item matching id {id} not found"]
        }

    return payload