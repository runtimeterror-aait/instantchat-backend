from flask import Response, request, jsonify
from flask_restful import Resource, abort, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.fields import EmbeddedDocumentField

from instantChat.models.user import User as UserModel, Contacts
# project resources
from instantChat.api.error import forbidden

from instantChat.api.includes import searchIndex


class ContactsResource(Resource):
    @jwt_required()
    def get(self) -> Response:
        authUser = UserModel.objects.get(id=get_jwt_identity())
        contacts = authUser.contacts
        return jsonify({'data': contacts})

    @jwt_required()
    def post(self) -> Response:
        data = request.get_json()
        user = UserModel.objects.get(id=get_jwt_identity())
        contact = Contacts(**data)
        user.contacts.append(contact)
        user.save()
        return jsonify({'data': user.contacts})


class ContactResource(Resource):
    @jwt_required()
    def get(self, contact_id) -> Response:
        contacts = UserModel.objects.get(id=get_jwt_identity()).contacts
        for contact in contacts:
            if str(contact.id) == contact_id:
                return jsonify({'data': contact})

        return jsonify({'message': "contact doesn't exist"})

    @jwt_required()
    def put(self, contact_id: str) -> Response:

        data = request.get_json()
        user = UserModel.objects.get(id=get_jwt_identity())

        for i in range(0, len(user.contacts)):
            if str(user.contacts[i].id) == contact_id:
                user.contacts[i].name = data['name']
                user.contacts[i].phone = data['phone']
                user.save()
                return jsonify({'message': 'Contact updated'})
        return jsonify({'message': 'Contact doesn\'t exist'})

    @jwt_required()
    def delete(self, contact_id: str) -> Response:
        user = UserModel.objects.get(id=get_jwt_identity())

        for i in range(0, len(user.contacts)):
            if str(user.contacts[i].id) == contact_id:
                del user.contacts[i]
                user.save()
                return jsonify({'message': 'Contact Deleted'})
        return jsonify({'message': 'Contact doesn\'t exist'})
