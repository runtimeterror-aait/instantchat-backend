import functools
from instantChat.api.includes import searchContacts, searchIndex

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_restful import Api

# project resources
from instantChat.api.auth import SignUpApi, LoginApi
from instantChat.resources.user import UserResource
from instantChat.resources.contact import ContactsResource, ContactResource, SearchChatRooms, SearchChatRooms
from instantChat.resources.contact import SearchContacts

bp = Blueprint("routes", __name__, url_prefix="/v1/api")
api = Api(bp)

api.add_resource(SignUpApi, '/auth/register')
api.add_resource(LoginApi, '/auth/login')

api.add_resource(UserResource, '/user/<user_id>')
api.add_resource(ContactsResource, '/contacts')
api.add_resource(ContactResource, '/contact/<contact_id>')
api.add_resource(SearchContacts, '/search/contacts/<search_term>')
api.add_resource(SearchChatRooms, '/search/chatrooms/<search_room>')