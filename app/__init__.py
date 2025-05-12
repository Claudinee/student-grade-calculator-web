# from flask import Flask

# def create_app():
#     app = Flask(__name__)

#     from .routes import main
#     app.register_blueprint(main)

#     return app
from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='../static')  # Ensures static folder is found

    from .routes import main
    app.register_blueprint(main)

    return app
