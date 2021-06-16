import os
from re import S
import re
from flask import Flask, app
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_mongoengine import MongoEngine

from secrets import token_urlsafe
from flask_cors import CORS
import time
from flask_socketio import SocketIO
# from flask_socketio import close_room, join_room, leave_room, emit
# print("================> START OF __init__app")

db = MongoEngine() #mk
jwt = JWTManager() #mk
socket = SocketIO()

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/*": {"origins": "*"}})

    socket.init_app(app, cors_allowed_origins="*")

    # config = {
    # 'MONGODB_SETTINGS': {
    #     'db': 'instantChat',
    #     'host': 'localhost',
    #     'port': 27017,
    # },
    # 'JWT_SECRET_KEY': 'instantChatKey'
    # }
    config = {
    'MONGODB_SETTINGS': {
        'db': 'bmbni9iduxoifkf',
        'host': 'mongodb://ullxngscsr8pmavwdoia:seAjYXu2i8x5MJrCRAyg@bmbni9iduxoifkf-mongodb.services.clever-cloud.com:27017/bmbni9iduxoifkf',
    },
    'JWT_SECRET_KEY': 'instantChatKey'
    # 'JWT_SECRET_KEY': token_urlsafe(16) #later
    }
    app.config.update(config)

    # load config variables
    if 'MONGODB_URI' in os.environ:
        app.config['MONGODB_SETTINGS'] = {'host': os.environ['MONGODB_URI'],
                                          'retryWrites': False}
    if 'JWT_SECRET_KEY' in os.environ:
        app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    db.init_app(app) #mk

    jwt.init_app(app) #mk
    
    from instantChat.api import routes

    app.register_blueprint(routes.bp)

    app.add_url_rule('/', endpoint='index')

    @app.route("/")
    # def hello():
    def index():
        return "hello, world"


# ###############################################See Frontend############################################
#     @socket.on('online')
#     def online(data):
#         recentMessages = {}; #db fetch... here #tbd
#         emit('recentMessages', recentMessages, brodcast = False, include_self = True); #include_self #tbch

#         #//to receive messages from all chats //join all their room
#         #// rooms = Object.keys(recentMessages); //#temp or not
#         #// socket.join(rooms);  //should work #tbtested
#         room_ids = [room_id for room_id in recentMessages.keys()]
#         join_room(room_ids)
        
#         #sending messages to all contacts to let them know the logged in user is online
#         for contact in data.conids: #also in front end #fnd
#             emit('userOnline', data.userid, to = contact)
        
        
        
#     @socket.on('offline')
#     def offline(data):
#         #db here... last seen (like UPDATE TABLE USERS COLUMN lastSeen to 'timestamp')
#         for contact in data.conids: #also in front end #fnd
#             emit('userOffline', {"userid": data.userid, "lastSeen": data.lastSeen}, to = contact)

    
        

#     @socket.on('getlastMessages')
#     def lastMessages(chatid):
#         lastMessages = {}; #db fetch... here #tbd
#         emit('lastMessages', lastMessages, brodcast = False, include_self = True); #tbcheck

#     @socket.on('sendMessage')
#     def sendMessage(msg):
#         #db here... add message
#         emit('message', msg, to = msg.room);


#     @socket.on('deleteChat') #haven't included callback
#     def deleteChat(data):
#         #db here...
        
#         #if succesful
#         emit('chatDeleted', data.chatid, to = data.chatid)   
#         close_room(data.chatid);


#     @socket.on('deleteMessage')
#     def deleteMessage(data):
#         #db here...
#         emit('messageDeleted', data, to = data.chatid)





#     ##################################################################################################

    
    # print("================> END OF __init__app.create_app")    
    return app

# print("================> END OF __init__app")  

