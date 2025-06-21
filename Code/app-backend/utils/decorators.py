from functools import wraps
from flask import abort 
from flask import request,jsonify
from flask import current_app as app
import jwt

def token_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        token=request.headers.get('Authorization')

        if not token:
            return {'message':"Token is Missing"},401
        
        try:
            decoded_token=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return {'message':'Token has expired'},401
        except jwt.InvalidTokenError:
            return {'message':'Invalid token'},401
        
        return f(decoded_token,*args,**kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(decoded_token,*args,**kwargs):
        if 'user' not in decoded_token['roles']:
            return {'message' : 'Admin Access required'},403
        return f(decoded_token,*args,**kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(decoded_token,*args,**kwargs):
        if 'admin' not in decoded_token['roles']:
            return {'message' : 'Admin Access required'},403
        return f(decoded_token,*args,**kwargs)
    return decorated_function
            
            
