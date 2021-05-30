import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_restful import Api

from instantChat.resources.Todo import TodoList

bp = Blueprint("todos", __name__, url_prefix="/v1/api")
api = Api(bp)

api.add_resource(TodoList, '/todo')
    
@bp.route("/hello1")
def hello():
    return "hello world"