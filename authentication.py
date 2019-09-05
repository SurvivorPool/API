from functools import wraps
from flask import request
import firebase_admin
from firebase_admin import auth
from dotenv import load_dotenv

import os
from models.user import UserModel
from models.playerTeam import PlayerTeamModel
load_dotenv(verbose=True)
cert = firebase_admin.credentials.Certificate({
    "type":
    "service_account",
    "project_id":
    os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id":
    os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key":
    os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email":
    os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id":
    os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri":
    os.getenv('FIREBASE_AUTH_URI'),
    "token_uri":
    os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url":
    os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url":
    os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
})
default_app = firebase_admin.initialize_app(cert)


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            auth.verify_id_token(request.headers['auth'])
        except:
            return {'message': 'Unable to authenticate'}, 403

        return f(*args, **kwargs)

    return decorated_func


def login_required_pass_along_user_id(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            request_user_info = auth.verify_id_token(request.headers['auth'])

        except:
            return {'message': 'Unable to authenticate'}, 403

        kwargs['authenticated_user_id'] = request_user_info['user_id']

        return f(*args, **kwargs)

    return decorated_func


def user_and_session_match_url_param(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):

        try:
            request_user_info = auth.verify_id_token(request.headers['auth'])
        except:
            return {'message': 'Unable to authenticate'}, 403

        user = UserModel.find_by_user_id(request_user_info['user_id'])
        if user is None or user.user_id != (kwargs['user_id']):
            return {'message': 'You are not the owner of this account.'}, 403


        return f(*args, **kwargs)
    return decorated_func


def user_and_session_match_json_param(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            request_user_info = auth.verify_id_token(request.headers['auth'])
        except:
            return {'message': 'Unable to authenticate'}, 407

        request_data = request.get_json()
        user = UserModel.find_by_user_id(request_data['user_id'])

        if user is None or user.user_id != request_user_info['user_id']:
            return {'message': 'You are not the owner of this account.'}, 403

        return f(*args, **kwargs)

    return decorated_func


def player_team_ownership_required_url_param(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            request_user_info = auth.verify_id_token(request.headers['auth'])
            team = PlayerTeamModel.find_by_team_id(kwargs['team_id'])

        except:
            return {'message': 'Unable to authenticate'}, 403

        if team is None or team.user_id != request_user_info['user_id']:
            return {'message': 'You are not the owner of this team.'}, 403

        return f(*args, **kwargs)

    return decorated_func


def player_team_ownership_required_json_param(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        request_user_info = auth.verify_id_token(request.headers['auth'])
        request_data = request.get_json()
        if "team_id" in request_data:
            team = PlayerTeamModel.find_by_team_id(request_data['team_id'])
        if team is None:
            return {'message': 'Team not found'}, 403

        if team.user_id != request_user_info['user_id']:
            return {'message': 'You are not the owner of this team.'}, 403


        return f(*args, **kwargs)

    return decorated_func


def admin_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):

        try:
            request_user_info = auth.verify_id_token(request.headers['auth'])
        except:
            return {'message': 'User not an administrator.'}, 403

        user = UserModel.find_by_user_id(request_user_info['user_id'])
        if not user.is_admin:
            return {'message': 'User not an administrator.'}, 403

        return f(*args, **kwargs)

    return decorated_func
