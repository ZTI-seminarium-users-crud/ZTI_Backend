from ariadne import convert_kwargs_to_snake_case

from api.models import Person


def listStudents_resolver(obj, info, limit=10, offset=0):
    try:
        students = [student.to_dict() for student in Person.query.slice(offset, offset+limit).all()]
        total_count = Person.query.count()
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
def getStudents_resolver(obj, info, id):
    try:
        student = Person.query.get(id)
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