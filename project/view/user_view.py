import datetime
from flask import Blueprint, request
from flask.views import MethodView
import jwt

from db.db import DB_request

user_blueprint = Blueprint("user", __name__)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, "rats", algorithm='HS512')


def check_token(token):
    data = jwt.decode(token, "rats", algorithms=['HS512'])
    return data.get("user_id", None)



class User(MethodView):
    def get(self):
        answer = {}
        status_code = 400
        token = str(request.headers.get("authorization", ""))
        if token == "" and not token.startswith("Bearer") and not token.split(" ")[1]:
            answer['message'] = "Please provide the token"
            status_code = 422
        else:
            user_id = check_token(token.split(" ")[1])
            rows = DB_request.get_user_by_id(user_id)
            if len(rows) > 0:
                answer['users'] = rows
                status_code = 200
            else:
                answer['message'] = "No user found"
                status_code = 422
        
        return answer, status_code
    

user_blueprint.add_url_rule("/getuser", view_func = User.as_view("user"))