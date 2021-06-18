#messages.py
#resource

# flask packages

import time
from instantChat.models.user import User
import re
from instantChat.models.chatRoom import ChatRoom
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import  cross_origin

from instantChat.models.message import TextMessage as UserMessage #edited

# project resources

class Messages(Resource):
    @jwt_required()
    def get(self)->Response:
        messages = UserMessage.objects.get_or_404(id=get_jwt_identity())
        # textMessage = authUser.textMessage
        return jsonify({'data': messages})


    @jwt_required()
    def post(self) -> Response:
        # print("=================> POST <=================")
                # x = get_jwt_identity()
                # return jsonify({"h": str(x)})
                # return jsonify({"h":"Hello"})

        try:
            data = request.get_json()
        except Exception as err:
            print(err)
            return jsonify({"Message":"Bad request", "Error": str(err)})

        try:
            data['sender'] = get_jwt_identity()
            data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
            # print("=========>TRY<==========")
            if not ChatRoom.objects(id=data['chatRoom']):
                return jsonify({"message":"No chatroom with the given id."})
            textMessage = UserMessage(**data) #???
            # textMessage = UserMessage(sender=data["sender"], receiver=data["receiver"], chatRoom=data["chatRoom"], timestamp=data[]) #???
            textMessage.save()
            # from instantChat.api_realtime import postMessages
            # postMessages(textMessage)
            return jsonify({"newMessage": textMessage}) #changed
        except Exception as err:
            # print("=========>Exception<==========")
            return jsonify({"error": str(err)})

# class Messages(Resource):
#     @jwt_required()
#     def get(self, message_id: str)-> Response:
#         Umessages = UserMessage.objects.get(id=get_jwt_identity()).Umessages
#         for msg in Umessages:
#             if str(msg.id) == message_id:
#                 return jsonify({'data': msg})
#         return jsonify({'message': "Message not found"})

#     @jwt_required()
#     def put(self, message_id: str)->Response:
#         data = request.get_json()
#         user_message = UserMessage.objects.get(id=get_jwt_identity())
#         textmessage = UserMessage.objects(id=message_id)
#         textmessage.update(**data)
#         return jsonify({'data': user_message.textmessage})

#     @jwt_required()
#     def delete(self, message_id: str) -> Response:
#         authUser = UserMessage.objects.get(id=get_jwt_identity())
#         delete_message = UserMessage.objects(id=message_id)
#         delete_message.delete()
#         return jsonify({'data': delete_message})
        

class Message(Resource):
    @jwt_required()
    def get(self, individual_id:str) -> Response:
        messages = UserMessage.objects.get_or_404(id=individual_id)
        return jsonify({'data': messages})


####################################################################
def getRoomIDs(userID):
    '''get a list of all the ids of rooms the user is a member of'''

    room_ids = []
    for room in ChatRoom.objects: #for every room
        # print(room.id)
        for userid in room["members"]: #for every member of the room
            # print(str(userid.id))
            # print(str(userID))
            # print('before if')
            if str(userID) == str(userid.id): #if the user is a member
                # print("in")
                room_ids.append(str(room["id"])) #add the id of the room to the room_ids list
    return room_ids

def getRecentMessage(roomIds):
    ''' gives a dictionary where the latest messages documents are values and the corresponding chat room names, the keys.'''
    recentMessages = []
    accounted = []

                    # for room in ChatRoom.objects:
                    #     room_ids.append(room.id)
                    #     recentMessages[room.id] = TextMessage.objects.(chatRoom=room.id).order_by("-timestamp").first()
    
    ChatRoomCount = len(roomIds) #number of chatRooms
    # print(ChatRoomCount)
    userid = str(User.objects.get(id=get_jwt_identity()).id)
    for message in UserMessage.objects.order_by("-timestamp"): #all messages ordered from latest to old
        # print("===")
        # print(str(message["chatRoom"].id))
        # print(len(recentMessages))
        # print("before first if")
        if len(recentMessages) == ChatRoomCount: #if all chatRooms have been accounted for
            break
        # print(accounted)
        # print(roomIds)
        # print("before second if")
        if (str(message["chatRoom"].id) not in accounted) and (str(message["chatRoom"].id) in roomIds): #if chatRoom not already accounted for and if the user is a member of it
            members = ChatRoom.objects.get_or_404(id=message["chatRoom"].id).members
            chatName = members[1].username if (str(members[0].id) == userid) else members[0].username
            # print(chatName)
            # recentMessages[chatName] = message;
            recentMessages.append({"name": chatName,"message": message.message, "timestamp": message.timestamp, "chatRoom": str(message.chatRoom.id)})
            accounted.append(str(message.chatRoom.id))
            # room_ids.append(message.chatRoom) #there might be rooms with zero messages
    # recentMessages = {}; #db fetch... here #tbd

    return recentMessages

def getlastRoomMessages(roomID):
    return UserMessage.objects(chatRoom=roomID).order_by("timestamp")[:15] #get the latest/last 25 messages from this room #assuming chatRoom field is id...


class RecentMessages(Resource):
    @jwt_required()
    # @cross_origin()
    def get(self) -> Response:
        # x = getRoomIDs(get_jwt_identity())
        # y = getRecentMessage(x)
        # print(y)
        # return jsonify([str(room_id) for room_id in getRoomIDs(get_jwt_identity())])
        return jsonify(getRecentMessage(getRoomIDs(get_jwt_identity())))

class LastMessages(Resource):
    @jwt_required()
    def get(self, room_id:str) -> Response:
        return jsonify(getlastRoomMessages(room_id))

 