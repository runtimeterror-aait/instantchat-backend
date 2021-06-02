from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.user import User as UserModel
from instantChat.models.chatRoom import ChatRoom as ChatRoomModel
# project resources
from instantChat.api.error import forbidden

class ChatRooms(Resource):
    #all chatRooms
    @jwt_required()
    def get(self, page) -> Response:
        #paginated
        chatRooms = ChatRoomModel.objects.paginate(page=page, per_page=10)

    @jwt_required()
    def post(self) -> Response:
        
        user = UserModel.objects.get(id=get_jwt_identity())
        data = request.get_json()
        membersList = [UserModel.objects(id=userId) for userId in data.members]
        new = {
            "name": data["name"],
            "description": data["description"],
            "owner": user,
            "members": membersList,
            "privateMessaging": bool(data["privateMessaging"])
        }
        newChatRoom = ChatRoomModel(**new)
        newChatRoom.save()
        return jsonify({"data": newChatRoom})

    @jwt_required()
class ChatRoom(Resource):
    pass