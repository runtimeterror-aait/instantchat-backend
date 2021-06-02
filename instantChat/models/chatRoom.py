from mongoengine import Document, EmbeddedDocument
from mongoengine import *
from flask import jsonify
from mongoengine.fields import ListField
from instantChat.models.user import User
from instantChat.models.message import Message

class ChatRoom(Document):
    name = StringField() #chat room name 
    description = StringField()
    owner = ReferenceField(User)
    members = ListField(ReferenceField(User)) #Only twi if its private
    privateMessaging = BooleanField()
