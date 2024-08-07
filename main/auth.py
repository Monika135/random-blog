from flask import Blueprint, request, jsonify, session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
# from flask_session import Session
from datetime import timedelta, datetime
from .models import Users
from . import post
from app import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
import re

auth = Blueprint('auth', __name__)


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[\W_]', password):
        return False
    return True


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    try:

        if request.method == 'POST' :
            required_fields = ['username', 'email', 'password', 'first_name']

            user_required_data = {
                "username": request.form.get("username"),
                "email": request.form.get("email"),
                "password": request.form.get("password"),
                "first_name": request.form.get("first_name"),
            }

            user_optional_data = {
                "last_name": request.form.get("last_name")
            }

            missing_fields = [field for field in required_fields if not user_required_data.get(field)]
            if missing_fields:
                return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}","status":"error"}), 400

            if not is_valid_email(user_required_data['email']):
                return jsonify({"message":"Invalid email format", "status":"error",}), 400
            
            if not is_valid_password(user_required_data['password']):
                return jsonify({"message":"Invalid password format,need to have atleast uppercase letter,special characters,lowercase,length must be greater than 8","status":"error"
                }),400

        

            hashed_password = bcrypt.generate_password_hash(user_required_data['password']).decode('utf-8')

            new_user = Users(
                    username= user_required_data['username'],
                    email= user_required_data['email'], 
                    password=  hashed_password,
                    first_name = user_required_data['first_name'],
                    last_name = user_optional_data['last_name'],
                    registeredTime = datetime.now()
                )

            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message":"Successfully registered","status":"success"}), 200
        
        elif request.method == 'GET':
            return jsonify({"message":"Need to Signup","status":"pending"}),202
    
    except IntegrityError:

        db.session.rollback()
        return jsonify({"message":"Username already exists","status":"error"}), 400

        
              

@auth.route('/login', methods=['POST'])
def login():

    # if session.get('user'):
    #     return jsonify({"status":"Invalid","message":"Already logged in"}), 401
    
    
        
        if request.method == 'POST':

            required_fields = ['username', 'password']

            user_data = {
                "username" : request.form.get("username"),
                "password" :   request.form.get("password")
            }

            missing_fields = [field for field in required_fields if not user_data.get(field)]
            if missing_fields:
                return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}","status": "error"}), 400

            else:
                user = Users.query.filter_by(username= user_data['username']).first()
                
                if user and bcrypt.check_password_hash(user.password, user_data['password']):
                        #session['user'] = user.username
                        access_token = create_access_token(identity = user.user_id, expires_delta=timedelta(hours=24))
                        refresh_token = create_refresh_token(identity = user.user_id, expires_delta=timedelta(days=7))

                        redirect_url = url_for('post.all_post')
                        return jsonify({
                                        "message":"Successfully logged in",
                                        "tokens" :{
                                        "access":access_token,
                                        "refresh":refresh_token,
                                        "url_for_posts": redirect_url,
                                        "status":"success"
                                    }
                        
                        }), 200
                
                
                return jsonify({"message":"Username or password is invalid","status":"error"}), 400
                
        
        


# @auth.route('/logout',methods=['GET'])
# @jwt_required()
# def logout():
#     #session['user'] = None
#     return jsonify({"status":"Success","message":"Succesfully logout"}), 201


    