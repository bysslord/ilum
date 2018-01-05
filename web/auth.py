#!/usr/bin/python
# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from functools import wraps

from util.db.user import User

__author__ = 'xiwei'

from web import get_params, Required, BaseError, app, g


def generate_auth_token(user, expiration=600):
    s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user.id}).decode("utf-8")


def auth(_token) -> User:
    s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(_token)
    except SignatureExpired:
        raise BaseError('Token expired', 401)
    except BadSignature:
        raise BaseError('Invalid token', 401)
    user = User.query.get(data['id'])
    return user


def token(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        _token = get_params(params=(("token", str, Required, None),)).get('token')
        g.user = auth(_token)
        return func(*args, **kwargs)

    return wrapper


def client_id(func):
    return func
