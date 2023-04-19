from .models import Students
from ariadne import convert_kwargs_to_snake_case


def listStudents_resolver(obj, info):
    try:
        students = [student.to_dict() for student in Students.query.all()]
        print(students)
        payload = {
            "success": True,
            "students": students
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def getStudents_resolver(obj, info, id):
    try:
        student = Students.query.get(id)
        payload = {
            "success": True,
            "students": student.to_dict()
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo item matching id {id} not found"]
        }

    return payload