from mongoengine import Document, EmbeddedDocument
from mongoengine import *
from flask import jsonify
from mongoengine.fields import CachedReferenceField, ListField, LongField, StringField, ReferenceField, BooleanField
from instantChat.models.user import User

class ChatRoom(Document):
    name = StringField() #chat room name 
    description = StringField()
    owner = ReferenceField(User)
    members = ListField(ReferenceField(User)) #Only twi if its private
    # membersCount = LongField() #to keep count of members #also userful to calc Popular Chat Rooms
    privateMessaging = BooleanField()

    # def save(self, *args, **kwargs):
    #     # Overwrite Document save method to increment membersCount every time a user is added to the chat room
    #     if self._created:
    #         # ChatRoom.objects(id=self.id).update_one(inc__membersCount=1)
    #         # self.membersCount += 1;
    #         # self.membersCount = ChatRoom.Objects(id = self.id).membersCount + 1;
    #     super(User, self).save(*args, **kwargs)
