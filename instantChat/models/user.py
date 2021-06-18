
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import *
from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

import re


class PhoneField(StringField):

    REGEX = re.compile(r"/^(^\+251|^251|^0)?9\d{8}$/")

    def validate(self, value):
        # Overwrite StringField validate method to include regex phone number check.
        if not PhoneField.REGEX.match(string=value):
            return jsonify({"error": f"ERROR: `{value}` Is An Invalid Phone Number."})
            self.error(f"ERROR: `{value}` Is An Invalid Phone Number.")
        super(PhoneField, self).validate(value=value)


class UserPhotos(EmbeddedDocument):
    imagePath = StringField()
    profilePicture = BooleanField(default=False)


class Contacts(EmbeddedDocument):
    id = SequenceField()
    name = StringField(required=True)
    phone = PhoneField(required=True)
    userId = StringField(required=True)


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    phone = PhoneField(required=True, unique=True)
    password = StringField(required=True, min_length=6, regex=None)
    bio = StringField()
    online = BooleanField()
    lastSeen = DateTimeField()
    deactivate = BooleanField()
    profilePicture = ListField(EmbeddedDocumentField(UserPhotos))
    contacts = ListField(EmbeddedDocumentField(Contacts))

    def generate_pw_hash(self):
        self.password = generate_password_hash(
            password=self.password).decode('utf-8')

    def check_pw_hash(self, password: str) -> bool:
        return check_password_hash(pw_hash=self.password, password=password)

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        if self._created:
            self.generate_pw_hash()
        super(User, self).save(*args, **kwargs)
