from api import app

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.explorer import ExplorerGraphiQL
from flask import request, jsonify
from api.queries import listStudents_resolver, getStudents_resolver
from api.mutations import create_student_resolver, update_student_resolver, delete_student_resolver

query = ObjectType("Query")
mutation = ObjectType("Mutation")
explorer_html = ExplorerGraphiQL().html(None)

query.set_field("listStudents", listStudents_resolver)
query.set_field("getStudents", getStudents_resolver)

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