from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.base.fields import ObjectIdField

from instantChat.models.user import User as UserModel
# project resources
from instantChat.api.error import forbidden


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id: str) -> Response:
        if user_id == "self":
            output = UserModel.objects.get(id=get_jwt_identity())
        else:
            try:
                output = UserModel.objects.get(phone=user_id)
            except:
                print("==================> not phone <===========")
                # if output.count() == 0:
                print(user_id)
                print(UserModel)
                try:
                    output = UserModel.objects.get(id=user_id) #ObjectId(user_id) ?
                    # output = UserModel.objects.get(id=ObjectID(user_id))
                    return jsonify({'data': output})
                except:
                    return jsonify({'message': "No user with the given id"})
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
        post_user = UserModel(**data).save()
        output = {'id': str(post_user.id)}
        return jsonify({'result': output})

    @jwt_required()
    def delete(self, user_id: str) -> Response:
        output = UserModel.objects(id=user_id).delete()
        return jsonify({'result': output})
