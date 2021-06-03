# flask packages
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.message import Message as Usermessage,TextMessage

# project resources
from models.message import Messages
# from models.users import Users
# from api.errors import forbidden

class messages(Resource):
    @jwt_required
    def get(self)->Response:
        authUser = Usermessage.objects.get(id=get_jwt_identity())
        TextMessage = authUser.TextMessage
        return jsonify({'data':TextMessage})
        

    @jwt_required
    def post(self)-> Response:
        data = request.get_json()
        user_message = Usermessage.objects.get(id=get_jwt_identity())
        textMessage = TextMessage(**data)
        user_message.TextMessage.append(textMessage)
        user_message.save()
        return jsonify({'data': user_message.TextMessage})


 