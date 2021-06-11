from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.user import User as UserModel
# project resources
from instantChat.api.error import forbidden

# print("================> START OF user.py")  

class UserResource(Resource):
    # @jwt_required()
    def get(self, user_id: str) -> Response:
        if user_id == "self":
            output = UserModel.objects.get_or_404(id=get_jwt_identity())
        else:
            output = UserModel.objects.get_or_404(phone=user_id)
            if output.count() == 0:
                output = UserModel.objects.get_or_404(id=user_id)
                return jsonify({'data': output})
        return jsonify({'data': output})

    @jwt_required()
    def put(self, user_id: str) -> Response:
        data = request.get_json()
        put_user = UserModel.objects(id=user_id).update(**data)
        output = {'id': str(put_user.id)}
        return jsonify({'result': output})

    @jwt_required()
    def post(self) -> Response:
        data = request.get_json()
        post_user = UserModel(**data).save() #created a user? by a logged in user? #mk
        output = {'id': str(post_user.id)}
        return jsonify({'result': output})

    @jwt_required()
    def delete(self, user_id: str) -> Response:
        output = UserModel.objects(id=user_id).delete() #delete any user? by a logged in user? #mk
        return jsonify({'result': output})
