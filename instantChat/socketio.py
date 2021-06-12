from instantChat.models.user import User
import time
from flask_jwt_extended.utils import get_jwt_identity
from werkzeug.datastructures import CharsetAccept
from instantChat import socket
from flask_socketio import close_room, join_room, leave_room, emit
from instantChat.models.message import TextMessage
from instantChat.models.chatRoom import ChatRoom

user_id = get_jwt_identity()


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
    return TextMessage.Objects.get_or_404(chatRoom=roomID).order_by("-timestamp")[:15] #get the latest/last 25 messages from this room #assuming chatRoom field is id...

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

###############################################See Frontend############################################
room_ids = []; contactChat_ids = [];
@socket.on('online')
def online(data):
    #assuming all messages fields are in TextMessage Document
    
    room_ids = getRoomIDs(user_id)
    recentMessages = getRecentMessage(room_ids)
    
    emit('recentMessages', {"recentMessages":recentMessages}, brodcast = False, include_self = True); #include_self #tbch

    room_ids = [room_id for room_id in recentMessages.keys()]
    join_room(room_ids)
    
    #sending messages to all contacts to let them know the logged in user is online
    contactChat_ids = getContactChatIDs(room_ids)
    for contactChat_id in contactChat_ids: #for each contactChat id
        emit('userOnline', {"user_id": user_id}, to = contactChat_id, include_self = False)
    
    #sending all online contacts of the user
    onlineContact_ids = getOnlineContactIDs(user_id, contactChat_ids)
    emit('onlineContacts', {"onlineContact_ids":onlineContact_ids}, brodcast = False, include_self = True); #add to #front end #tbd! #!
    
    #setting the user status to online (the boolean field in the user document)
    setOnlineField(user_id, True)


@socket.on('offline')
def offline(data): #data #frontend
    setLastSeenField(user_id, toDbDateFormat(data.lastSeen))#(like UPDATE TABLE USERS COLUMN lastSeen to 'timestamp')

    for contactChat_id in contactChat_ids:
        emit('userOffline', {"user_id": user_id, "lastSeen": data.lastSeen}, to = contactChat_id)


    

@socket.on('getlastMessages')
def lastMessages(data): #data
    lastMessages = getlastRoomMessages(data.room_id);
    emit('lastMessages', {"lastMessages":lastMessages}, brodcast=False, include_self=True); #tbcheck

@socket.on('sendMessage')
def sendMessage(data): #data
    addMessage(data.message, data.timestamp, data.chatroom, receiver_id=data.receiver_id) #db here... add message
    emit('message', {"message": data.message, "timestamp": data.timestamp}, to= data.chatroom) #would have liked to have changed the field name from chatroom to chatroom_id or room_id or chat_id


@socket.on('deleteChat') #haven't included callback
def deleteChat(data): #data
    if deleteRoom(data.room_id, user_id):
        emit('chatDeleted', {"room_id":data.room_id}, to = data.room_id, include_self = True) #frontend notification, for, user needs confirmation
        close_room(data.room_id);
    else:
        emit('notOwner', {"data": "You are unauthorized to delete the room as you are not its owner."}, to = data.room_id, include_self = True, brodcase = False)


@socket.on('deleteMessage')
def deleteMessage(data): #data
    if deleteRoomMessage(data.message_id, user_id):#db here...
        emit('messageDeleted', {"message_id":data.message_id}, to = data.room_id, include_self = True) #frontend notification, for, user needs confirmation
    else:
        emit('notAuthorized', {"data": "You are unauthorized to delete the message as you are it's author or the owner of the room."}, to = data.room_id, include_self = True, brodcase = False)





    ##################################################################################################