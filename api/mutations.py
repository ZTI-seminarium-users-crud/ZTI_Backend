from datetime import date

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Student


@convert_kwargs_to_snake_case
def create_student_resolver(obj, info, first_name, last_name, age, average_grade, degree, hair_color, height, is_male, semester, specialization, weight):
    try:
        today = date.today()
        student = Student(
            first_name=first_name, last_name=last_name, specialization=specialization, degree=degree, semester=semester, age=age, average_grade=average_grade, hair_color=hair_color, height=height, is_male=is_male, weight=weight
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
def update_student_resolver(obj, info, id, first_name, last_name, age, average_grade, degree, hair_color, height, is_male, semester, specialization, weight):
    try:
        student = Student.query.get(id)
        if student:
            student.first_name = first_name
            student.last_name = last_name
            student.specialization = specialization
            student.degree = degree
            student.semester = semester
            student.age = age
            student.average_grade = average_grade
            student.hair_color = hair_color
            student.height = height
            student.is_male = is_male
            student.weight = weight
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