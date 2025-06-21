from flask import Flask, redirect, request,flash,url_for,jsonify
from flask import current_app as app
from flask_bcrypt import Bcrypt 
import jwt
from models.models import db,User
from functools import wraps
from utils.decorators import token_required,user_required
import datetime
from app import cache,new_user_email



bcrypt = Bcrypt()
users=[]

@app.route("/", methods=["GET", "POST"])
def start():
    return ('Hello, Flask App')

#signup API
@app.route('/api/register',methods=["POST"])
def register():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    email_id=data.get('email')
    format='HTML'
    from models.models import User,Role,RoleAssignment
    user_p=User.query.filter_by(username=username).first()
    if user_p:
        return jsonify({'message':"Username already taken,try a different one !"}),409

    email_p=User.query.filter_by(email_id=email_id).first()
    if email_p:
        return jsonify({'message':"Email Already Registered"}),409
    hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
    #new user
    user=User(username=username,password_hash=hashed_password,email_id=email_id,format=format)
    role = Role.query.filter_by(role_name='user').first()
    role_assignment=RoleAssignment(user=user,role=role)
    db.session.add(user)
    db.session.add(role_assignment)
    db.session.commit()
    new_user_email.delay(user.user_id)
    return jsonify(message='User Registered Successfully,Go on Login and Enjoy'),201


#Login API
@app.route('/api/login',methods=['POST'])
def login():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    from models.models import User,RoleAssignment,Role
    user=User.query.filter_by(username=username).first()
    if(user):
        role_assignment=RoleAssignment.query.filter_by(user_id=user.user_id).first()
        role_id=role_assignment.role_id
        role=Role.query.filter_by(role_id=role_id).first()
        name=role.role_name
    if not user:
        return jsonify(message="Invalid Credentials,Username does not exist"),401
    
    if bcrypt.check_password_hash(user.password_hash,password):
        expiration_time=datetime.datetime.utcnow()+datetime.timedelta(minutes=90)
        token=jwt.encode({'username':username,'roles':name,'exp':expiration_time},app.config['SECRET_KEY'],algorithm='HS256')
        return jsonify(token=token,username=username,role=name),200
    
    return jsonify(message="Invalid Credentials"),401


#get the role of the user
@app.route('/api/user/role',methods=['GET'])
@token_required
def get_role(decoded_token):
    role=decoded_token['roles']
    return jsonify({'role':role})

#to get the details for user profile 
@app.route('/api/user/profile',methods=['GET'])
@token_required
def get_profile(decoded_token):
    username=decoded_token['username']
    user=User.query.filter_by(username=username).first()
    if(user):
        email=user.email_id
        return jsonify(username=username,email=email),201
    else:
        return jsonify(message="No user Found"),404
    


#logout api 
@app.route('/api/logout',methods=['GET'])
def logout():
    return redirect('/')


#changing the format of user monthly entertainment report 
@app.route('/api/user/reportformat',methods=['POST'])
@token_required
@user_required
def change_report_format(decoded_token):
    username=decoded_token['username']
    user=User.query.filter_by(username=username).first()
    data=request.get_json()
    format=data['format']
    user.format=format
    db.session.commit()
    return ({'message':'Successfuly changed Monthly Report Format'}),201