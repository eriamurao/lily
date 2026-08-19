import os

from flask import Flask



def create_app(test_config=None):
  # create the app and configure the app

  # __name__ is the name of the current module and the app needs to know where it is
  # instance_relative_config tells the app that when app.config.from_pyfile(...) is called,
  #   look for the config file in the instance folder
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  os.makedirs(app.instance_path, exist_ok=True)

  # a simple page that says hello
  @app.route('/hello')
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
