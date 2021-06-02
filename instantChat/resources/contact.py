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
                return jsonify({'data':contact})
            else:
                return jsonify({'data': "contact doesn't exist"}) 
                
    @jwt_required()
    def put(self, contact_id: str) -> Response:

        data = request.get_json()
        user = UserModel.objects.get(id=get_jwt_identity(), contacts__id=contact_id)
        put_user = user.contacts.objects(id=contact_id).update(**data)

        return jsonify({'result': put_user})
        #  post = Post.objects.get(title="Quora rocks", comments__name="john").update(set__comment__S__name="John)

    @jwt_required()
    def delete(self, user_id: str) -> Response:
        user = Users.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            output = Meals.objects(id=user_id).delete()
            return jsonify({'result': output})
        else:
            return forbidden()
