from flask import Response, json, request, jsonify
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
        membersList = [UserModel.objects(id=userId) for userId in data["members"]][0] #//whhy [0]? #mk
        
        new = {
            "name": data["name"],
            "description": data["description"],
            "owner": user,
            "members": membersList,
            "privateMessaging": bool(data["privateMessaging"])
        }
        newChatRoom = ChatRoomModel(**new)
        newChatRoom.save()
        # from instantChat.api_realtime import postChatRooms
        # postChatRooms(newChatRoom)

        return jsonify({"data": newChatRoom})



class ChatRoom(Resource):
    @jwt_required()
    def get(self, chat_room_id) -> Response:
        try:
            chatRoom = ChatRoomModel.objects.get(id=chat_room_id)
        except:
            return jsonify({'message': "No chat room be the first to create one"})
        return jsonify({'data': chatRoom})

    # //add users
    @jwt_required()
    def post(self, chat_room_id) -> Response:
        data = request.get_json()
        newMembersList = [UserModel.objects(
            id=userId) for userId in data.members]

        for member in newMembersList:
            if ChatRoomModel.objects.get(id=chat_room_id, members=member).count() == 0:
                ChatRoomModel.objects.get(id=chat_room_id).members.append(member)
        
        # from instantChat.api_realtime import postChatRoom
        # postChatRoom(newMembersList, chat_room_id)

        return jsonify({"message": "New members has been added"})

    @jwt_required()
    def put(self, chat_room_id) -> Response:
        data = request.get_json()
        loggedInUser = UserModel.objects.get(id=get_jwt_identity())
        chatRoom = ChatRoomModel.objects.get(id=chat_room_id)
        if chatRoom.owner == loggedInUser:
            chatRoom.update(**data)
            # chatRoom.save() #why save
            return jsonify({"data": chatRoom})
        else:
            return jsonify({"data": "you are not the owner of this chat room"})

    @jwt_required()
    def delete(self, chat_room_id) -> Response:
        loggedInUser = UserModel.objects.get(id=get_jwt_identity())
        chatRoom = ChatRoomModel.objects.get(id=chat_room_id)
        if chatRoom.owner == loggedInUser:
            chatRoom.delete()
            # from instantChat.api_realtime import deleteChatRoom
            # deleteChatRoom(chatRoom)
            return jsonify({"data": "Deleted successfully"})
        else:
            return jsonify({"data": "you are not the owner of this chat room"})


class PopularChatRoom(Resource):
    @jwt_required()
    def get(self) -> Response:
        # chatRoom = ChatRoomModel.objects.order_by("members").members[:6]
        # chatRoom = ChatRoomModel.objects.order_by("-members.length")[:6]

        # check and decide #mk #tb
        max = [-1,-1,-1,-1,-1,-1]
        room_ids = [-1,-1,-1,-1,-1,-1]
        for room in ChatRoomModel.objects.get_or_404(): #(privateMessaging=False) might help
            for i in range(max.length):
                if room.members.length > max[i]:
                    max = max[:i] + [room.members.length] + max[i:5] #shift right
                    room_ids = room_ids[:i] + [room.id] + room_ids[i:5] #shifts right together, while keeping track of ids
        if max[0] == 2: #since private messages are being counted, this might be a case
            chatRoom = "None"
            return jsonify({"data: chatRoom"})
        chatRoom = [] #to hold the 6 most popular rooms
        for room_id in room_ids:
            for room in ChatRoomModel.Objects.get_or_404(id=room_id):
                chatRoom.push(room)

        return jsonify({"data": chatRoom})
