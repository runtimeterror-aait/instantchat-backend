from flask import Flask


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    from instantChat import routes
    from instantChat import auth
    
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)
    
    app.add_url_rule('/', endpoint='index')
    
    return app
