from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from instantChat.models.user import User as UserModel
from instantChat.api.error import unauthorized

import datetime

class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            newUser = UserModel(**data)
            newUser.save()
            output = {'id': str(newUser.id)}
            return jsonify({'result': output})
        except:
            return jsonify({'message': "Bad request. User probably already exists."})



class LoginApi(Resource):

    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            user = UserModel.objects.get(email=data.get('email'))
        except:
            return jsonify({"message": "user doesn't exist"})
        auth_success = user.check_pw_hash(data.get('password'))
        if not auth_success:
            return unauthorized()
        else:
            expiry = datetime.timedelta(days=5)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'result': {'access_token': access_token,
                                       'refresh_token': refresh_token,
                                       'logged_in_as': f"{user.email}",
                                       'user_id': f"{user.id}"}
                                       })

