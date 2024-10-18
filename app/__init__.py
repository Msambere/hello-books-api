from flask import Flask

def create_app():
    app = Flask(__name__)

    #Register Blueprints here
    return app