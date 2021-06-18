import functools
from instantChat.resources.messages import LastMessages, Message, Messages, RecentMessages

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_restful import Api
# print("================> START OF routes.py")  
# project resources
from instantChat.api.auth import SignUpApi, LoginApi
from instantChat.resources.user import UserResource
from instantChat.resources.contact import ContactsResource, ContactResource
from instantChat.resources.chatRoom import ChatRooms, ChatRoom, PopularChatRoom
bp = Blueprint("routes", __name__, url_prefix="/v1/api")
api = Api(bp)

api.add_resource(SignUpApi, '/auth/register')
api.add_resource(LoginApi, '/auth/login')

api.add_resource(UserResource, '/user/<user_id>')
api.add_resource(ContactsResource, '/contacts')
api.add_resource(ContactResource, '/contact/<contact_id>')

api.add_resource(ChatRoom, '/chatRooms/<chat_room_id>')
api.add_resource(PopularChatRoom, '/chatRooms/popular')



api.add_resource(Messages, '/messages') #when post ... returns jsonify of TextMessage



api.add_resource(Message, '/messages/<individual_id>')

#POST
api.add_resource(ChatRooms, '/chatRooms/<contact_id>') #accepts contact_id and room data / POST, not json needed ## return jsonify({"chatRoomObject": newChatRoom, "room_id":newChatRoom.id, "confirmationMessage": newMessage})

#GET
api.add_resource(RecentMessages, '/messages/recent') # return jsonfiy of 
#recentMessages.push({"name": chatName,"message": message.message, "timestamp": message.timestamp, "chatroom": message.chatroom})
api.add_resource(LastMessages, '/messages/<room_id>') # returns jsonify of TextMessage