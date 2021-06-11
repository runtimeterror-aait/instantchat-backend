from instantChat import socket
from flask_socketio import close_room, join_room, leave_room, emit

###############################################See Frontend############################################
@socket.on('online')
def online(data):
    recentMessages = {}; #db fetch... here #tbd
    emit('recentMessages', recentMessages, brodcast = False, include_self = True); #include_self #tbch

    #//to receive messages from all chats //join all their room
    #// rooms = Object.keys(recentMessages); //#temp or not
    #// socket.join(rooms);  //should work #tbtested
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