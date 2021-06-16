from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from instantChat.models.user import User as UserModel
from instantChat.api.error import invalid_route, unauthorized, bad_input

import datetime

class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
        data = request.get_json()
        newUser = UserModel(**data)
        print(newUser)
        newUser.save()
        output = {'id': str(newUser.id)} #only the id? #mk #created recource uri based on ...
        # from instantChat.api_realtime import SignUpApi
        # SignUpApi(newUser)
        return jsonify({'result': output})


class LoginApi(Resource):

    @staticmethod
    def post() -> Response:
        data = request.get_json()
        # print(data)
        # print(request.data)
        if not data:
            # print("in no data", request)
            return bad_input()
        user = UserModel.objects.get_or_404(email=data.get('email'))
        auth_success = user.check_pw_hash(data.get('password'))
        if not auth_success:
            return unauthorized()
        else:
            expiry = datetime.timedelta(days=5)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id)) #manual expiry then or ... #mk
            return jsonify({'result': {'access_token': access_token,
                                       'refresh_token': refresh_token, #refresh_token sent #mk
                                       'logged_in_as': f"{user.email}"}}) #only the email? #mk things like pp for socket? still... hmm

