from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.user import User as UserModel
# project resources
from instantChat.api.error import forbidden

class ContactsResource(Resource):
    @jwt_required()
    def get(self) -> Response:

        authUser = UserModel.objects.get(id=get_jwt_identity())
        contacts = authUser.contacts
        return jsonify({'data': contacts})