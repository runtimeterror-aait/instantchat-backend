import re
from typing import NewType

from mongoengine.errors import DoesNotExist
from instantChat.models.user import User
import time
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended import jwt_required
from instantChat import socket
# from . import socket 
from flask_socketio import close_room, join_room, leave_room, emit
from instantChat.models.message import TextMessage
from instantChat.models.chatRoom import ChatRoom

# @jwt_required
# def getLoggedInUserID():
#     return get_jwt_identity()

# user_id = getLoggedInUserID()

user_id = "34"

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
    for message in TextMessage.object.order_by("-timestamp"): #all messages ordered from latest to old
        if len(recentMessages) == ChatRoomCount: #if all chatrooms haven't been accounted for
            break;
        if (message["chatroom"] not in recentMessages.keys()) and (message["chatroom"] in roomIds): #if chatroom not already accounted for and if the user is a member of it
            chatName = ChatRoom.Objects.get_or_404(id=message["chatroom"])["name"]
            recentMessages[chatName] = message;
            # room_ids.push(message.chatroom) #there might be rooms with zero messages
    # recentMessages = {}; #db fetch... here #tbd

    return recentMessages

def toDbDateFormat(frontEndDateFormat):
    date = time.strptime(frontEndDateFormat, '%b %d, %y %I:%M%p')
    dbDateFormat = time.strftime('%Y-%m-%d %H:%M', date)
    return dbDateFormat

def toFrontEndDateFormat(dbDateFormat):
    date = time.strptime(dbDateFormat, '%Y-%m-%d %H:%M')
    frontEndDateFormat = time.strftime('%b %d, %y %I:%M%p', date)
    return frontEndDateFormat

def getContactChatIDs(roomIds):
    ''' returns list of contact ids of the logged in user '''
    ''' Note: contact id here is not id of Contact Document/User but the id of the private chat room '''
    contact_ids = []
    for room in ChatRoom.Objects.get_or_404(privateMessaging=True): #for all private rooms
        if room.id in roomIds: #if the user is a member of it
            contact_ids.push(room.id)
    return contact_ids

def getOnlineContactIDs(userID, contactChatIds):
    onlineContactIds = []
    for room in ChatRoom.Objects.get_or_404(id=contactChatIds): #for every private room  (contact room)
        for member_Id in room.members: #for each members
            if member_Id != userID: #if the member is not the logged in user
                if (User.Object.get_or_404(id=member_Id))["online"] == True: #and if the user is online
                    onlineContactIds.push(member_Id)
    return onlineContactIds

def setOnlineField(userID, value): #for now only set 'online' of User field
    User.objects(id=userID).update(set__online=value)

def setLastSeenField(userID, value):
    User.objects(id=userID).update(set__lastSeen=value)

def getlastRoomMessages(roomID):
    return TextMessage.Objects.get_or_404(chatRoom=roomID).order_by("timestamp")[:15] #get the latest/last 25 messages from this room #assuming chatRoom field is id...

def addMessage(message, timestamp, chatroom, receiver_id = None, sender_id = user_id):
    newMessage = {
                "message": "{message}",
                "chatroom": "{chatroom}", #or just self? #q #tb
                "timestamp":  toDbDateFormat(timestamp),
                "sender": "{sender_id}"
            }
    if receiver_id:
        newMessage["receiver"] = "{receiver_id}"
    newMessage = TextMessage(**newMessage)
    newMessage.save()

def deleteRoom(roomID, userID):
    room = ChatRoom.Objects.get_or_404(id=roomID)
    if room.owner == userID:
        room.delete()
        return True
    return False

def deleteRoomMessage(messageID, userID):
    message = TextMessage.Objects.get_or_404(id=messageID)
    if message.sender == userID:# or message.chatroom.owner == userID: #q #would this work?
        message.delete()
        return True
    room = ChatRoom.Objects.get_or_404(id=message.chatroom)
    if room.owner == userID:
        message.delete()
        return True    
    return False


def createChatRoom(name, member_ids, timestamp, description = "Private Chat", owner_id = "", privateMessaging = "True"):
    ''' creates a chat room and sends a global system message on it confirming it's creation
        returns confirmation message and the id, and member ids of the room created '''
    member_ids.push(user_id) #frnt end must not send user_id
    if privateMessaging:
        newPrivateChat = ChatRoom(name = name, description = description, owner = owner_id, privateMessaging = privateMessaging, members = member_ids).save()
        globalconfirmationMessage = addMessage(message="Private Chat Successfully Created!", timestamp=timestamp, chatroom=newPrivateChat.id)
        return {"confirmation" : globalconfirmationMessage.message, "room_id":newPrivateChat.id, "member_ids": newPrivateChat.members}
    newGroupChat = ChatRoom(name = name, description = description, privateMessaging = privateMessaging, members = member_ids).save()
    globalconfirmationMessage = addMessage(message="Group Chat Successfully Created!", timestamp=timestamp, chatroom=newGroupChat.id)
    return {"message" : globalconfirmationMessage.message, "room_id":newGroupChat.id, "member_ids": newGroupChat.members}

# def user_id_of_username(userID): #for when username isnt pk
#     return

def roomExits(roomID):
    # return True if ChatRoom.Objects.get(id=roomID).count() == 1 else False #count returns 0 when there's no query result right? didn't use get_or_404 bc ... 404
    try:
        ChatRoom.Objects.get(id=roomID)
        return True
    except DoesNotExist:
        return True


def lg(log):
    print(log)

###############################################See Frontend############################################
room_ids = []; contactChat_ids = [];
@socket.on('online')
def online(data):
    #assuming all messages fields are in TextMessage Document
    print("on...line")
    print(data)
    
    # room_ids = getRoomIDs(user_id);
    room_ids = ["1","2"]
    lg(f'room_ids: {room_ids}')
    # recentMessages = getRecentMessage(room_ids); 
    recentMessages = [
        {"name":"Games","message":"roar", "timestamp":"May 23, 21 3:54PM", "chatroom":"324rt344"},
        {"name":"Games","message":"roar", "timestamp":"May 23, 21 3:54PM", "chatroom":"324rt344"},
        {"name":"Games","message":"roar", "timestamp":"May 23, 21 3:54PM", "chatroom":"324rt344"}
    ]
    lg(f'recentMessages: {recentMessages}')
    emit('recentMessages', {"recentMessages":recentMessages}, broadcast = False, include_self = True); #include_self #tbch

    # room_ids = [room_id for room_id in recentMessages.keys()]
    join_room(room_ids)
    
    #sending messages to all contacts to let them know the logged in user is online
    # contactChat_ids = getContactChatIDs(room_ids);
    contactChat_ids = ["1","2","3","4"]
    for contactChat_id in contactChat_ids: #for each contactChat id
        emit('userOnline', {"user_id": user_id}, to = contactChat_id, include_self = False)
    
    #sending all online contacts of the user
    # onlineContact_ids = getOnlineContactIDs(user_id, contactChat_ids);
    onlineContact_ids = ["3","4"]
    emit('onlineContacts', {"onlineContact_ids":onlineContact_ids}, broadcast = False, include_self = True); #add to #front end #tbd! #!
    lg(f'onlineContact_ids: {onlineContact_ids}')
    #setting the user status to online (the boolean field in the user document)
    # setOnlineField(user_id, True)


@socket.on('offline')
def offline(data): #data #frontend
    # setLastSeenField(user_id, toDbDateFormat(data["lastSeen"]))#(like UPDATE TABLE USERS COLUMN lastSeen to 'timestamp')

    for contactChat_id in contactChat_ids:
        emit('userOffline', {"user_id": user_id, "lastSeen": data["lastSeen"]}, to = contactChat_id)


# //------------------------------------create, join chats---------------------------------//
#createPrivateChat event
#createGroupChat event
#joinChat 

 


#for both private and group
@socket.on('createChat')
def createChat(data): #data json #if private chat, don't send in owner_id, etc, now even as Null -- send ONLY the other member in a list, and name (user choosen) #always including timestamp
    # confimation = createChatRoom(**data)
    confirmation = {"member_ids": ["4","5","7"],"room_id":"3","message": "Private Chat Created."}
    # room_ids.push(confimation.room_id);
    room_ids.push("3")
    #members need to join the group
    # join_room(confimation.room_id);
    join_room("3")
    emit('newChat', {"member_ids": confirmation.member_ids, "room_id":confirmation.room_id, "message": confirmation.message}, broadcast = True, include_self = False) #will improve it #frnt end should reply with their id and the room id if they are members (no problem for offline members since ... db) => joingChat, that is, messages too

    emit('chatCreated', {"confirmation": confirmation.message}, to=confirmation.room_id, include_self = True)


@socket.on('joiningChat')
def joiningChat(data): #data #user id / member id and room id and message
    # if user_id == data["user_id"]: #security check
    if True:
        # join_room(data["room_id"])
        join_room("3")
        emit('joinedChat', {"message": data["message"]}, include_self=True, broadcast=False) #must be handled exactly like chatCreated in the front end so ... use functions for the same code
        # emit('chatCreated', {"confirmation": confimation.confirmation}, to=confimation.room_id, include_self = True) #if it works, use this #check #tbchk
     

# @socket.on('createGroupChat')
@socket.on('joinChat')
def joinChat(data):
    if roomExits(data["room_id"]): #a check #security check
    # if True:
        join_room(data["room_id"])
        emit("joinedRoom", {"room_id":data["room_id"]}, broadcast = False, include_self = False) #front end will have to then open the chat, emit openChat, causing messages to be fetched from db ...
    else:
        emit("roomDoesntExist", {"error" : "Room doesn't exist"}, include_self=True, broadcast=True) #should be implemented in the front end after everything else




# //------------------------------------Open chat---------------------------------//
    

@socket.on('getlastMessages')
def lastMessages(data): #data
    # lastMessages = getlastRoomMessages(data["room_id"]);
    lastMessages = [{"message": "Oy", "timestamp":"Jun 12, 21 4:45AM"}] #test
    emit('lastMessages', {"lastMessages":lastMessages}, broadcast=False, include_self=True); #tbcheck





# --------------------------------------------------------send Message-----------------------------#

@socket.on('sendMessage')
def sendMessage(data): #data
    print("sendMessage")
    # addMessage(data["message"], data["timestamp"], data["chatroom"], receiver_id=data["receiver_id"]) #db here... add message
    emit('message', {"message": data["message"], "timestamp": data["timestamp"]}, to= data["chatroom"]) #would have liked to have changed the field name from chatroom to chatroom_id or room_id or chat_id





#---------------------------------------------delet Chat, Message------------------------------#

@socket.on('deleteChat') #haven't included callback
def deleteChat(data): #data
    if deleteRoom(data["room_id"], user_id):
    # if True:
        emit('chatDeleted', {"room_id":data["room_id"]}, to = data["room_id"], include_self = True) #frontend notification, for, user needs confirmation
        close_room(data["room_id"]);
    else:
        emit('notOwner', {"data": "You are unauthorized to delete the room as you are not its owner."}, to = data["room_id"], include_self = True, broadcast = False)


@socket.on('deleteMessage')
def deleteMessage(data): #data
    if deleteRoomMessage(data["message_id"], user_id):#db here...
    # if True:
        emit('messageDeleted', {"message_id":data["message_id"]}, to = data["room_id"], include_self = True) #frontend notification, for, user needs confirmation
    else:
        emit('notAuthorized', {"data": "You are unauthorized to delete the message as you are it's author or the owner of the room."}, to = data["room_id"], include_self = True, broadcast = False)





    ##################################################################################################