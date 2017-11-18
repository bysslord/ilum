#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'xiwei'

from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from .. import app, route, Required, get_params, request, BaseError
from flask import jsonify
from util.db.user import User
from util.db import db


def generate_auth_token(user, expiration=600):
    s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user.id})


def auth(token) -> User:
    s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        raise BaseError('Token expired', 401)
    except BadSignature:
        raise BaseError('Invalid token', 401)
    user = User.query.get(data['id'])
    return user


@app.route('/account/register', methods=['POST'])
def account_register():
    params = get_params(
        (
            ('username', str, Required, None),
            ('password', str, Required, None)
        ), request.json
    )
    username, password = params.get('username'), params.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        return f'User {username} has already exists', 400
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return generate_auth_token(user)


@app.route('/account/login', methods=['POST'])
def account_login():
    params = get_params(
        (
            ('username', str, Required, None),
            ('password', str, Required, None)
        ), request.json
    )
    username, password = params.get('username'), params.get('password')
    user = User.query.filter_by(username=username).first()
    if not user:
        raise BaseError(f'User {username} not found', 404)
    if not user.verify(password):
        raise BaseError(f'Password error', 400)
    return generate_auth_token(user)


@app.route('/account/info', methods=['POST'])
def account_info():
    params = get_params(
        (
            ('token', str, Required, None),
        ), request.json
    )

    token = params.get('token')
    user = auth(token)
    return jsonify(user_id=user.user_id, username=user.username)
