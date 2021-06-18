from typing import cast
from instantChat.models.message import TextMessage
from flask import Response, json, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.user import User as UserModel
from instantChat.models.chatRoom import ChatRoom as ChatRoomModel
# project resources
from instantChat.api.error import forbidden
import time


class ChatRooms(Resource):
    # all chatRooms
    @jwt_required()
    def get(self) -> Response:
        chatRooms = ChatRoomModel.objects
        return jsonify({'data': chatRooms})


#################################################################################
    @jwt_required()
    def post(self, contact_id: str) -> Response: #accepts contact_id and chatRoom data

        user = UserModel.objects.get(id=get_jwt_identity())
        # data = request.get_json()
        # membersList = [UserModel.objects(id=userId) for userId in data["members"]][0] #//whhy [0]? #mk
        membersList = [user]
        # print('\n')
        # print(membersList[0])
        # print('\n')
        contact = {}
        try:
            # print(contact_id)
            # print(UserModel)
            contact = UserModel.objects.get(id=contact_id)
        except Exception as err:
            print("==================> contact doesn't exist <===============")
            print(err)
            return jsonify({"message":"No contact with the given id"})
        membersList.append(contact)
        new = {
            # "name": data["name"],
            # "description": data["description"],
            # "owner": user,
            "members": membersList,
            # "privateMessaging": bool(data["privateMessaging"])
            # "privateMessaging": True
        }
        newChatRoom = ChatRoomModel(**new)
        try:
            newChatRoom.save()
        except Exception as err:
            print("========> chat already exits <========")
            print(err)
            return jsonify({"message":"The chat already exists, i.e. with the two members."})

        newMessage = {
                "message": "Private Chat Successfully Created!",
                "chatRoom": newChatRoom.id, #or just self? #q #tb
                # "timestamp":  toDbDateFormat(timestamp),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "sender": user.id,
                "receiver": contact_id
        }
        newMessage = TextMessage(**newMessage)

        #last bc ...
        # newChatRoom.save() #have to put it ^^ bc newMesssag needs the id, which is generated afer .save
        newMessage.save()
        # from instantChat.api_realtime import postChatRooms
        # postChatRooms(newChatRoom)

        return jsonify({"chatRoomObject": newChatRoom, "room_id": str(newChatRoom.id), "confirmationMessage": newMessage}) #obj, id, obj
#################################################################################


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
        try:
            chatRoom = ChatRoomModel.objects.get(id=chat_room_id)
        except Exception as err:
            print(err)
            return jsonify({"message":"Chat doesn't exist.", "Error": str(err)})
        # if chatRoom.owner == loggedInUser:
        if True:
            chatRoom.delete()
            # from instantChat.api_realtime import deleteChatRoom
            # deleteChatRoom(chatRoom)
            TextMessage.objects(chatRoom=chat_room_id).delete()
            return jsonify({"message": "Deleted successfully"})
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
        for room in ChatRoomModel.objects: #(privateMessaging=False) might help
            for i in range(len(max)):
                if len(room.members) > max[i]:
                    max = max[:i] + [len(room.members)] + max[i:5] #shift right
                    room_ids = room_ids[:i] + [room.id] + room_ids[i:5] #shifts right together, while keeping track of ids
        if max[0] == 2: #since private messages are being counted, this might be a case
            return jsonify({"data": "All chatrooms have only 2 members"})
        chatRooms = [] #to hold the 6 most popular rooms
        for room_id in room_ids:
            for room in ChatRoomModel.objects(id=room_id):
                chatRooms.append(room)

        return jsonify({"data": chatRooms})
