
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import *

from instantChat.models.user import User

class Token(Document):
    token = StringField(required=True)
    refreshToken = StringField(required=True) 
    user = ReferenceField(User, reverse_delete_rule=True)
    