from datetime import date

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Student


@convert_kwargs_to_snake_case
def create_student_resolver(obj, info, first_name, last_name, specialization, degree, semester):
    try:
        today = date.today()
        student = Student(
            first_name=first_name, last_name=last_name, specialization=specialization, degree=degree, semester=semester
        )
        db.session.add(student)
        db.session.commit()
        payload = {
            "success": True,
            "student": student.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload

@convert_kwargs_to_snake_case
def update_student_resolver(obj, info, id, first_name, last_name, specialization, degree, semester):
    try:
        student = Student.query.get(id)
        if student:
            student.first_name = first_name
            student.last_name = last_name
            student.specialization = specialization
            student.degree = degree
            student.semester = semester
        db.session.add(student)
        db.session.commit()
        payload = {
            "success": True,
            "post": student.to_dict()
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }

    return payload

@convert_kwargs_to_snake_case
def delete_student_resolver(obj, info, id):
    try:
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        payload = {"success": True, "post": student.to_dict()}

    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }

    return payload