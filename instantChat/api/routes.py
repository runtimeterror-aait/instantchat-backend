import functools
from instantChat.resources.user import UsersResource

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_restful import Api

# project resources
from instantChat.api.auth import SignUpApi, LoginApi
from instantChat.resources.user import UserResource, UsersResource

bp = Blueprint("routes", __name__, url_prefix="/v1/api")
api = Api(bp)

api.add_resource(SignUpApi, '/auth/register/')
api.add_resource(LoginApi, '/auth/login/')

api.add_resource(UsersResource, '/user/')
api.add_resource(UserResource, '/user/<user_id>')

# api.add_resource(MealsApi, '/meal/')
# api.add_resource(MealApi, '/meal/<meal_id>')