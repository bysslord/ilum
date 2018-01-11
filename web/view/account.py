#!/usr/bin/python
# -*- coding: utf-8 -*-
from web import auth

__author__ = 'xiwei'

from .. import app, Required, get_params, request, BaseError
from util.db.user import User
from util.db import db


@app.route('/api/v1/account/register', methods=['POST'])
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
    return auth.generate_auth_token(user)


@app.route('/api/v1/account/login', methods=['POST'])
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
    return auth.generate_auth_token(user)


@app.route('/api/v1/account/info', methods=['POST'])
@auth.token
def account_info():
    params = get_params(
        (
            ('token', str, Required, None),
        ), request.json
    )
    return params

