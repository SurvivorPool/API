from functools import wraps
from flask import request
import firebase_admin
from firebase_admin import auth, credentials

cred = credentials.Certificate('serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)

def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        #print(request.headers['auth'])
        try:
            print(auth.verify_id_token(request.headers['auth']))
            auth.verify_id_token(request.headers['auth'])
            return f(*args, **kwargs)
        except:
            return {'message': 'Unable to authenticate'}, 403
        #print(args)
    return decorated_func
