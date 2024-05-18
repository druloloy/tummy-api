from firebase_admin import auth, initialize_app
from firebase_admin._user_mgt import UserRecord
from functools import wraps
from flask import request
from globals.error.error_handler import handle_errors
from globals.error.exception import TummyError
from firebase.certficate import Certificate

cred = Certificate()
fb = initialize_app(cred)

def firebase_auth(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        token = authorization.split(" ")[1]

        if not token:
            return handle_errors(TummyError("No token provided", 401))
        
        try:
            decoded_token = auth.verify_id_token(token, app=fb)
            user: UserRecord = auth.get_user(decoded_token['user_id'], app=fb)
            return f(*args, **kwargs, fb_user=user)
        except Exception as e:
            return handle_errors(e)
    return decorated