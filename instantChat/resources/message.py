# flask packages
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.message import Message as Usermessage,TextMessage

# project resources
from api.errors import forbidden

class messages(Resource):
    @jwt_required
    def get(self)->Response:
        authUser = Usermessage.objects.get(id=get_jwt_identity())
        TextMessage = authUser.TextMessage
        return jsonify({'data':TextMessage})
        

    @jwt_required
    def post(self) -> Response:
        data = request.get_json()
        user_message = Usermessage.objects.get(id=get_jwt_identity())
        textMessage = TextMessage(**data)
        user_message.TextMessage.append(textMessage)
        user_message.save()
        return jsonify({'data': user_message.TextMessage})


class messages(Resource):
    @jwt_required
    def get(self, message_id: str) -> Response:
        authUser = Usermessage.objects.get(id=get_jwt_identity())
        TextMessage = authUser.TextMessage
        return jsonify({'data':TextMessage})


    @jwt_required
    def put(self, message_id: str)->Response:
        data = request.get_json()
        user_message = Usermessage.objects.get(id=get_jwt_identity())
        textmessage = TextMessage.objects(id=message_id)
        textmessage.update(**data)
        return jsonify({'data': user_message.textmessage})

    @jwt_required
    def delete(self, message_id: str) -> Response:
        authUser = Usermessage.objects.get(id=get_jwt_identity())
        delete_message = Usermessage.objects(id=message_id)
        delete_message.delete()
        return jsonify({'data': delete_message})
        

class message(Resource):
    @jwt_required()
    def get(self, individual_id) -> Response:
        messages = Usermessage.objects.get(id=individual_id)
        return jsonify({'data': messages})

 