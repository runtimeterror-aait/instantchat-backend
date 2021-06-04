from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.user import User as UserModel
from instantChat.models.chatRoom import ChatRoom as ChatRoomModel
# project resources
from instantChat.api.error import forbidden


class ChatRooms(Resource):
    # all chatRooms
    @jwt_required()
    def get(self) -> Response:
        chatRooms = ChatRoomModel.objects
        return jsonify({'data': chatRooms})

    @jwt_required()
    def post(self) -> Response:

        user = UserModel.objects.get(id=get_jwt_identity())
        data = request.get_json()
        membersList = [UserModel.objects(id=userId) for userId in data.members]
        new = {
            "name": data["name"],
            "description"PopularChatRoom: data["description"],
            "owner": user,
            "members": membersList,
            "privateMessaging": bool(data["privateMessaging"])
        }
        newChatRoom = ChatRoomModel(**new)
        newChatRoom.save()
        return jsonify({"data": newChatRoom})

    # @jwt_required()


class ChatRoom(Resource):
    @jwt_required()
    def get(self, chat_room_id) -> Response:
        chatRoom = ChatRoomModel.objects.get(id=chat_room_id)
        return jsonify({'data': chatRoom})

    @jwt_required()
    def put(self, chat_room_id) -> Response:
        data = request.get_json()
        loggedInUser = get_jwt_identity()
        chatRoom = ChatRoomModel.objects.get(id=chat_room_id)
        if chatRoom.owner == loggedInUser:
            chatRoom.update(**data)
            chatRoom.save()
            return jsonify({"data": chatRoom})
        else:
            return jsonify({"data": "you are not the owner of this chat room"})

    @jwt_required()
    def delete(self, chat_room_id) -> Response:
        loggedInUser = get_jwt_identity()
        chatRoom = ChatRoomModel.objects.get(id=chat_room_id)
        if chatRoom.owner == loggedInUser:
            chatRoom.delete()
            return jsonify({"data": "Deleted successfully"})
        else:
            return jsonify({"data": "you are not the owner of this chat room"})

class PopularChatRoom(Resource):
    @jwt_required()
    def get(self) -> Response:
        chatRoom = ChatRoomModel.objects
        return jsonify({"data": chatRoom})