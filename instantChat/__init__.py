import os
from re import S
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

import time
from flask_socketio import SocketIO, close_room, join_room, leave_room, emit

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    socket = SocketIO(app)

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
    }
    app.config.update(config)

    # load config variables
    if 'MONGODB_URI' in os.environ:
        app.config['MONGODB_SETTINGS'] = {'host': os.environ['MONGODB_URI'],
                                          'retryWrites': False}
    if 'JWT_SECRET_KEY' in os.environ:
        app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    db = MongoEngine(app)

    jwt = JWTManager(app)
    
    from instantChat.api import routes

    app.register_blueprint(routes.bp)

    app.add_url_rule('/', endpoint='index')

    @app.route("/")
    # def hello():
    def index():
        return "hello, world"


    ###########################################See Frontend############################################
    @socket.on('connect')
    def connect():
        recentMessages = {}; #db fetch... here #tbd
        emit('recentMessages', recentMessages, brodcast = False, include_self = True); #include_self #tbch

    @socket.on('getlastMessages'):
    def lastMessages(chatid):
        lastMessages = {}; #db fetch... here #tbd
        emit('lastMessages', lastMessages, brodcast = False, include_self = True); #tbcheck

    @socket.on('sendMessage')
    def sendMessage(msg):
        #db here... add message
        emit('message', msg, to = msg.room);


    @socket.on('deleteChat') #haven't included callback
    def deleteChat(data):
        #db here...
        
        #if succesful
        emit('chatDeleted', data.chatid, to = data.chatid)   
        close_room(data.chatid);



    ##################################################################################################

    
        
    return app

