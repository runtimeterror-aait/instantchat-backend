from mongoengine import Document
from mongoengine.fields import StringField,EmailField

class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True);

