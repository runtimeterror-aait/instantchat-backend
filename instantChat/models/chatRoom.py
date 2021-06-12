from flask_mongoengine import BaseQuerySet
from mongoengine import Document, EmbeddedDocument
from mongoengine import *
from flask import jsonify
from mongoengine.fields import CachedReferenceField, ListField, LongField, StringField, ReferenceField, BooleanField
from instantChat.models.user import User
from instantChat.models.message import TextMessage

import time

class ChatRoom(Document):
    name = StringField() #chat room name 
    description = StringField()
    owner = ReferenceField(User)
    members = ListField(ReferenceField(User)) #Only twi if its private #including owner
    # membersCount = LongField() #to keep count of members #also userful to calc Popular Chat Rooms
    privateMessaging = BooleanField()
    meta = {'queryset_class': BaseQuerySet}

    def save(self, *args, **kwargs):
        # Overwrite Document save method to add a message saying "Chat created" when created
    #     # Overwrite Document save method to increment membersCount every time a user is added to the chat room
        if self._created:
            # ChatRoom.objects(id=self.id).update_one(inc__membersCount=1)
    #         # self.membersCount += 1;
    #         # self.membersCount = ChatRoom.Objects(id = self.id).membersCount + 1;
            createMessage = {
                "message": "Chat created",
                "chatroom": self.id, #or just self? #q #tb
                "timestamp": time.strftime('%b %d, %y %I:%M%p', time.localtime())
            }
            createMessage = TextMessage(**createMessage)
            createMessage.save()
        super(User, self).save(*args, **kwargs)
