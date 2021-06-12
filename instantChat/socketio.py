from flask_jwt_extended.utils import get_jwt_identity
from werkzeug.datastructures import CharsetAccept
from instantChat import socket
from flask_socketio import close_room, join_room, leave_room, emit
from instantChat.models.message import TextMessage
from instantChat.models.chatRoom import ChatRoom

user_id = get_jwt_identity()


def roomIDs(userID):
    '''get a list of all the ids of rooms the user is a member of'''

    room_ids = []
    for room in ChatRoom.Objects.get_or_404(): #for every room
        if userID in room["members"]: #if the user is a member
            room_ids.push(room["id"]) #add the id of the room to the room_ids list
    return room_ids


def recentMessage(roomIds):
    ''' gives a dictionary where the latest messages documents are values and the corresponding chat room names, the keys.'''
    recentMessages = {}

                    # for room in ChatRoom.Objects:
                    #     room_ids.push(room.id)
                    #     recentMessages[room.id] = TextMessage.objects.get_or_404(chatRoom=room.id).order_by("-timestamp").first()
    
    ChatRoomCount = len(room_ids) #number of chatrooms
    for message in TextMessage.object.order_by("-timestamp"): #all messages ordered from latest to old
        if len(recentMessages) == ChatRoomCount: #if all chatrooms haven't been accounted for
            break;
        if (message["chatroom"] not in recentMessages.keys()) and (message["chatroom"] in roomIds): #if chatroom not already accounted for and if the user is a member of it
            chatName = ChatRoom.Objects.get_or_404(id=message["chatroom"])["name"]
            recentMessages[chatName] = message;
            # room_ids.push(message.chatroom) #there might be rooms with zero messages
    # recentMessages = {}; #db fetch... here #tbd

    return recentMessages

###############################################See Frontend############################################
@socket.on('online')
def online(data):
    #assuming all messages fields are in TextMessage Document
    
    room_ids = roomIDs(user_id)
    recentMessages = recentMessage(room_ids)
    
    emit('recentMessages', recentMessages, brodcast = False, include_self = True); #include_self #tbch

    room_ids = [room_id for room_id in recentMessages.keys()]
    join_room(room_ids)
    
    #sending messages to all contacts to let them know the logged in user is online
    for contact in data.conids: #also in front end #fnd
        emit('userOnline', data.userid, to = contact)
    
    
    
@socket.on('offline')
def offline(data):
    #db here... last seen (like UPDATE TABLE USERS COLUMN lastSeen to 'timestamp')
    for contact in data.conids: #also in front end #fnd
        emit('userOffline', {"userid": data.userid, "lastSeen": data.lastSeen}, to = contact)


    

@socket.on('getlastMessages')
def lastMessages(chatid):
    lastMessages = {}; #db fetch... here #tbd
    emit('lastMessages', lastMessages, brodcast = False, include_self = True); #tbcheck

@socket.on('sendMessage')
def sendMessage(msg):
    #db here... add message
    emit('message', msg, to = msg.room);


@socket.on('deleteChat') #haven't included callback
def deleteChat(data):
    #db here...
    
    #if succesful
    emit('chatDeleted', data.chatid, to = data.chatid)   
    close_room(data.chatid);


@socket.on('deleteMessage')
def deleteMessage(data):
    #db here...
    emit('messageDeleted', data, to = data.chatid)





    ##################################################################################################