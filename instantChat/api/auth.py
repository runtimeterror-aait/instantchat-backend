from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from instantChat.models.user import User as UserModel
from instantChat.models.token import Token as TokenModel
from instantChat.api.error import unauthorized

import datetime

class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        newUser = UserModel(**data)
        newUser.save()
        output = {'id': str(newUser.id)}
        return jsonify({'result': output})


class LoginApi(Resource):

    @staticmethod
    def post() -> Response:
        data = request.get_json()
        try:
            user = UserModel.objects.get(email=data.get('email'))
            auth_success = user.check_pw_hash(data.get('password'))
        except:
            auth_success = False
        if not auth_success:
            return unauthorized()
        else:
            expiry = datetime.timedelta(days=10)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            newToken = TokenModel(token=access_token, refreshToken=refresh_token, user=user)
            if newToken.save():
                return jsonify({'result': {'access_token': access_token,
                                       'refresh_token': refresh_token,
                                       'logged_in_as': f"{user.email}"}})
            else:
                return jsonify({'error': "Error Adding Token"})

class LogoutApi(Resource):
    @jwt_required()
    def get(self) -> Response:
        user = UserModel.objects.get(id=get_jwt_identity())
        token = TokenModel.objects.get(user=user)
        #  _revoke_current_token()()
        return jsonify({'data': token})
