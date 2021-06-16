#messages.py
#resource

# flask packages

from instantChat.models.chatRoom import ChatRoom
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from instantChat.models.message import TextMessage as UserMessage #edited

# project resources

class Messages(Resource):
    @jwt_required
    def get(self)->Response:
        messages = UserMessage.objects.get_or_404(id=get_jwt_identity())
        # textMessage = authUser.textMessage
        return jsonify({'data': messages})


    @jwt_required               
    def post(self) -> Response:
        data = request.get_json()
        textMessage = UserMessage(**data) #???
        # textMessage = UserMessage(sender=data["sender"], receiver=data["receiver"], chatRoom=data["chatRoom"], timestamp=data[]) #???
        textMessage.save()
        # from instantChat.api_realtime import postMessages
        # postMessages(textMessage)
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
        messages = UserMessage.objects.get_or_404(id=individual_id)
        return jsonify({'data': messages})


def getRoomIDs(userID):
    '''get a list of all the ids of rooms the user is a member of'''

    room_ids = []
    for room in ChatRoom.Objects.get_or_404(): #for every room
        if userID in room["members"]: #if the user is a member
            room_ids.push(room["id"]) #add the id of the room to the room_ids list
    return room_ids

def getRecentMessage(roomIds):
    ''' gives a dictionary where the latest messages documents are values and the corresponding chat room names, the keys.'''
    recentMessages = {}

                    # for room in ChatRoom.Objects:
                    #     room_ids.push(room.id)
                    #     recentMessages[room.id] = TextMessage.objects.get_or_404(chatRoom=room.id).order_by("-timestamp").first()
    
    ChatRoomCount = len(roomIds) #number of chatrooms
    for message in UserMessage.object.order_by("-timestamp"): #all messages ordered from latest to old
        if len(recentMessages) == ChatRoomCount: #if all chatrooms haven't been accounted for
            break;
        if (message["chatroom"] not in recentMessages.keys()) and (message["chatroom"] in roomIds): #if chatroom not already accounted for and if the user is a member of it
            chatName = ChatRoom.Objects.get_or_404(id=message["chatroom"])["name"]
            recentMessages[chatName] = message;
            # room_ids.push(message.chatroom) #there might be rooms with zero messages
    # recentMessages = {}; #db fetch... here #tbd

    return recentMessages

def getlastRoomMessages(roomID):
    return UserMessage.Objects.get_or_404(chatRoom=roomID).order_by("timestamp")[:15] #get the latest/last 25 messages from this room #assuming chatRoom field is id...


class RecentMessages(Resource):
    @jwt_required
    def get(self) -> Response:
        return jsonify({'data': getRecentMessage(getRoomIDs(get_jwt_identity()))})

class LastMessages(Resource):
    @jwt_required
    def get(self, room_id:str) -> Response:
        return getlastRoomMessages(room_id)

 