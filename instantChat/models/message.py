from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import *
from flask import jsonify
from instantChat.models.user import User
from instantChat.models.chatRoom import ChatRoom


class Message(Document):
    sender = ReferenceField(User)
    chatRoom = ReferenceField(ChatRoom)
    meta = {'allow_inheritance': True}

class TextMessage(Message):
    message = StringField(required=True)

class ImageMessage(Message):
    image_path = ListField(StringField())
