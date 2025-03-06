import hashlib
import re
from flask import Blueprint, request
from flask.views import MethodView
from db.db import DB_request

register_blueprint = Blueprint("register", __name__)

class Register(MethodView):
    def post(self):
        answer = {}
        status_code = 400
        json = request.json
        if len(json['name'].strip()) < 3:
            answer['error'] = "The name must be of minimum 3 characters"
            status_code = 422
            return answer, status_code
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', json["email"].strip()):
            answer['error'] = "Invalid email address"
            status_code = 422
            return answer, status_code
        
        if len(json['name'].strip()) < 4:
            answer['error'] = "The Password must be of minimum 4 characters length"
            status_code = 422
            return answer, status_code

        password = hashlib.sha512(json["password"].encode()).hexdigest()
        if DB_request.check_email(json["email"]):
            answer['error'] = 'user is already created'
            status_code = 422
        else: 
            DB_request.add_user(json['email'], json["name"].strip(), password)
            answer["message"] = 'user is create'
            status_code = 201
        
        return answer, status_code
    

register_blueprint.add_url_rule("/register", view_func = Register.as_view("register"))