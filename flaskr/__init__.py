import os

from flask import Flask

def create_app(test_config = None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True) # creates Flask instance
    app.config.from_mapping( #sets the default configuration that the app will use
        SECRET_KEY = 'dev', # used to keep the data safe
        DATABASE=os.path.join(app.instance_path, 'flaskr_sqlite'), # path where the SQLite database file will be saved
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True) # overrides the default configuration with values taken from the config.py 
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path) #  ensures that app.instance_path exists
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')# creates a simple route so you can see the application working
    def hello():
        return 'Hello, World!'



    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
