#messages.py
#resource

# flask packages

from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.message import TextMessage as UserMessage #edited

# project resources

class Messages(Resource):
    @jwt_required
    def get(self)->Response:
        authUser = UserMessage.objects.get(id=get_jwt_identity())
        # textMessage = authUser.textMessage
        return jsonify({'data': authUser})


    @jwt_required               
    def post(self) -> Response:
        data = request.get_json()
        textMessage = UserMessage(**data) #???
        textMessage.save()
        from instantChat.api_realtime import postMessages
        postMessages(textMessage)
        return jsonify({'data': textMessage})


# class Messages(Resource):
#     @jwt_required()
#     def get(self, message_id: str)-> Response:
#         Umessages = UserMessage.objects.get(ip=get_jwt_identity()).Umessages
#         for msg in Umessages:
#             if str(msg.id) == message_id:
#                 return jsonify({'data': msg})
#         return jsonify({'message': "Message not found"})

#     @jwt_required
#     def put(self, message_id: str)->Response:
#         data = request.get_json()
#         user_message = UserMessage.objects.get(id=get_jwt_identity())
#         textmessage = UserMessage.objects(id=message_id)
#         textmessage.update(**data)
#         return jsonify({'data': user_message.textmessage})

#     @jwt_required
#     def delete(self, message_id: str) -> Response:
#         authUser = UserMessage.objects.get(id=get_jwt_identity())
#         delete_message = UserMessage.objects(id=message_id)
#         delete_message.delete()
#         return jsonify({'data': delete_message})
        

class Message(Resource):
    @jwt_required()
    def get(self, individual_id:str) -> Response:
        messages = UserMessage.objects.get(id=individual_id).messages
        return jsonify({'data': messages})

 