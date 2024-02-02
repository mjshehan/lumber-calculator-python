from flask import Flask 
import os

def create_app():
    app = Flask(__name__) #represents name of the file
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    from .views import views
    from .auth import auth

    #app.register_blueprint(views, url_prefix='/' )
    app.register_blueprint(auth, url_prefix='/' )

    return app

