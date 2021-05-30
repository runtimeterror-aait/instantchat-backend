# from flask import g
# from flask_mongoengine import MongoEngine
# from mongoengine import connect
# from mongoengine.connection import disconnect

# def get_db():
#     g.db = MongoEngine()
#     return g.db
    
# def close_db(e=None):
    
#     db = g.pop("db", None)

#     if db is not None:
#         disconnect(alias="instantchat")

# def init_app(app):
#     app.config['MONGODB_SETTINGS'] = {
#         'db': 'instantchat',
#         'host': '127.0.0.1',
#         'port': 27017
#     }
#     get_db().init_app(app)
