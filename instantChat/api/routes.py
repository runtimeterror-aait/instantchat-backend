import functools
import re

from flask.json import jsonify
from flask_jwt_extended.utils import unset_access_cookies
from flask_jwt_extended.view_decorators import jwt_required
import jwt
from instantChat.models.message import TextMessage

from flask.wrappers import Response

from instantChat.resources.messages import LastMessages, Message, Messages, RecentMessages

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_restful import Api, Resource
# print("================> START OF routes.py")  
# project resources
from instantChat.api.auth import SignUpApi, LoginApi
from instantChat.resources.user import UserResource
from instantChat.resources.contact import ContactsResource, ContactResource
from instantChat.resources.chatRoom import ChatRooms, ChatRoom, PopularChatRoom
bp = Blueprint("routes", __name__, url_prefix="/v1/api")
api = Api(bp)

#[✔]
api.add_resource(SignUpApi, '/auth/register')
#[✔]
api.add_resource(LoginApi, '/auth/login')

#[✔]
api.add_resource(UserResource, '/user/<user_id>')
#[✔]
api.add_resource(ContactsResource, '/contacts')
api.add_resource(ContactResource, '/contact/<contact_id>')

# api.add_resource(ChatRoom, '/chatRooms')
api.add_resource(ChatRoom, '/chatRooms/<chat_room_id>')
api.add_resource(PopularChatRoom, '/chatRooms/popular')


#[Post - ✔]
api.add_resource(Messages, '/messages') #when post ... returns jsonify of TextMessage



api.add_resource(Message, '/message/<individual_id>')

#POST
#[✔]
api.add_resource(ChatRooms, '/chatRooms/contact/<contact_id>') #accepts contact_id and room data / POST, not json needed ## return jsonify({"chatRoomObject": newChatRoom, "room_id":newChatRoom.id, "confirmationMessage": newMessage})

#GET
#[✔]
api.add_resource(RecentMessages, '/messages/recent') # return jsonfiy of 
#recentMessages.append({"name": chatName,"message": message.message, "timestamp": message.timestamp, "chatRoom": message.chatRoom})
#[✔]
api.add_resource(LastMessages, '/messages/chatRoom/<room_id>') # returns jsonify of TextMessage


class Logout(Resource):
    @jwt_required()
    def get(self) -> Response:
        return unset_access_cookies(jsonify({"message":"Logged out."}))

api.add_resource(Logout, '/auth/logout')



class Test(Resource):
    def get(self) -> Response:
        t = TextMessage.objects.order_by('-timestamp').distinct('chatRoom')
        return jsonify(t)
api.add_resource(Test, '/test')