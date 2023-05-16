from api import app

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.explorer import ExplorerGraphiQL
from flask import request, jsonify
from api.queries import read_students_resolver, read_student_resolver
from api.mutations import create_student_resolver, update_student_resolver, delete_student_resolver

query = ObjectType("Query")
mutation = ObjectType("Mutation")
explorer_html = ExplorerGraphiQL().html(None)

query.set_field("readStudents", read_students_resolver)
query.set_field("readStudent", read_student_resolver)

mutation.set_field("createStudent", create_student_resolver)
mutation.set_field("updateStudent", update_student_resolver)
mutation.set_field("deleteStudent", delete_student_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.route("/student:<id>", methods=["GET"])
def read_record(id):

    result = read_student_resolver(None, None, id)

    if result["success"]:
        columns = request.args.get("columns")
        if columns is None:
            return result["student"]
        else:
            selected_columns = [item.strip() for item in columns.split(',')]
            return {key: result["student"][key] for key in selected_columns}
    else:
        return result["errors"]


@app.route("/filters/<filter>", methods=["GET"])
def read_filters(filter):
    try:
        f = open("api/filters/"+filter)
    except FileNotFoundError:
        return "Error. There's no such filter"
    else:
        with f:
            filter_values = [line.rstrip('\n') for line in f]
        return filter_values


@app.route("/students", methods=["GET"])
def read_page():

    specialization = request.args.get("specialization")
    degree = request.args.get("degree")
    semester = request.args.get("semester")
    page_size = request.args.get("pageSize")
    page_number = request.args.get("pageNumber")

    result = read_students_resolver(None, None,
                                    int(page_size) if page_size else 10,
                                    int(page_number)*int(page_size) if page_number and page_size else 0,
                                    [item.strip() for item in specialization.split(',')] if specialization else None,
                                    [item.strip() for item in degree.split(',')] if degree else None,
                                    [item.strip() for item in semester.split(',')] if semester else None)
    if result["success"]:
        columns = request.args.get("columns")
        if columns is None:
            return result["students"]
        else:
            selected_columns = [item.strip() for item in columns.split(',')]
            selected_result = []
            for student in result["students"]:
                record = {key: student[key] for key in selected_columns}
                selected_result.append(record)
            return selected_result
    else:
        return result["errors"]