import os

from flask import Flask


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)


    from instantChat import todo

    app.register_blueprint(todo.bp)
    
    app.add_url_rule('/', endpoint='index')
    

    return app
