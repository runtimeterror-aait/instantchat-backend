from flask_mongoengine import BaseQuerySet
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import *
from flask import jsonify
from instantChat.models.user import User
from instantChat.models.chatRoom import ChatRoom


##############################################################
class Message(Document):
    sender = ReferenceField(User) #for chatRoom created message
    receiver = ReferenceField(User) #isn't chatRoom enough?
    chatRoom = ReferenceField(ChatRoom, required=True)
    timestamp = DateTimeField()  #might not do gte, lte... like ComplexDateTimeField #%Y-%m-%d %H:%M #resources/messages.py will have to be updated
    meta = {'allow_inheritance': True}

##############################################################
class TextMessage(Message):
    message = StringField(required=True)
    meta = {'queryset_class': BaseQuerySet}

class ImageMessage(Message):
    image_path = ListField(StringField())
    meta = {'queryset_class': BaseQuerySet}