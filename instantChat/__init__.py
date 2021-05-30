import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
default_config = {
    'MONGODB_SETTINGS': {
        'db': 'instantChat',
        'host': 'localhost',
        'port': 27017,
        # 'username': 'admin',
        # 'password': 'password',
        # 'authentication_source': 'admin'
    },
    'JWT_SECRET_KEY': 'changeThisKeyFirst'}


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.update(default_config)

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

