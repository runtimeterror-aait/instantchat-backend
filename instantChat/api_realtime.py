# to be user by resources
from instantChat import socket
from flask_socketio import close_room, join_room, leave_room, emit

# def SignUpApi():

#     pass

def postMessages(textMessage):
    socket.emit('message', {"message": textMessage.message, "timestamp": textMessage.timestamp}, to=textMessage.chatRoom)


def postChatRooms(room):
    #~chatCreated
    pass

def postChatRoom(members, roomID):
    #if openedChat = ...
    pass

def deleteChatRoom(room):
    #remove 
    pass

# def postContactsResource(contact):
#     #not pm
#     pass

# def putContactResource(contact):
#     pass

# def deleteContactResource(contact):
#     pass


def putUserResource(user):
    pass