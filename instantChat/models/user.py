from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import *

# user photos 
class UserPhotos(EmbeddedDocument):
    imagePath = StringField()
    profilePicture = BooleanField(default=False)
class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    phone = IntField(required=True, unique=True)
    password = StringField(required=True)
    bio = StringField(required=True)
    online = BooleanField(required=True)
    lastSeen = DateTimeField()
    deactivate = BooleanField(required=True)
    profilePicture = ListField(EmbeddedDocumentField(UserPhotos))




