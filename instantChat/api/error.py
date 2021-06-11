# flask packages
from flask import Response, jsonify


def unauthorized() -> Response:
    output = {"error":
              {"message": "401 error: The email or password provided is invalid."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 401
    return resp


def forbidden() -> Response:
    output = {"error":
              {"message": "403 error: The current user is not authorized to take this action."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 403
    return resp


def invalid_route() -> Response:
    output = {"error":
              {"message": "404 error: This route is currently not supported. See API documentation."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 404
    return resp

def bad_input() -> Response:
    output = {"error":
              {"message": "400 error: Bad input."}
              }
    resp = jsonify({'result': output})
    resp.status_code = 400
    return resp
