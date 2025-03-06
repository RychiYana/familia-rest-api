import datetime
from flask import Blueprint, request
from flask.views import MethodView
import jwt

from db.db import DB_request

login_blueprint = Blueprint("login", __name__)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, "rats", algorithm='HS512')


class Login(MethodView):
    def post(self):
        answer = {}
        status_code = 400
        json = request.json
        
        if not DB_request.check_user(json["email"], json["password"]):
            answer['error'] = 'invalid email or password'
            status_code = 422
        else:
            user_id = DB_request.get_user(json["email"], json["password"])
            token = generate_token(user_id)
            answer['token'] = token
            status_code = 200
        
        return answer, status_code
    

login_blueprint.add_url_rule("/login", view_func = Login.as_view("login"))