from flask import g
from mongoengine import connect
from mongoengine.connection import disconnect

def get_db():
    db = connect('instantchat', host='127.0.0.1', port=27017) 
    g.db = db
    # connect('my_db', username='my_user', password='my_password', authentication_source='admin')

def close_db(e=None):
    
    db = g.pop("db", None)

    if db is not None:
        disconnect(alias="instantchat")

