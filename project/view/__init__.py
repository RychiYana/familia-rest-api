from flask import Flask
from view.login_view import login_blueprint
from view.register_view import register_blueprint
from view.user_view import user_blueprint

app = Flask(__name__)

app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(user_blueprint)

def start_server():
    app.debug = True
    return app