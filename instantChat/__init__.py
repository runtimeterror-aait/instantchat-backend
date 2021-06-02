import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

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
    def hello():
        return "hello, world"
        
    return app

