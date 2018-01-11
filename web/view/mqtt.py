#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from .. import app
from util.logger import log
from util.db.user import User
from flask import request


@app.route('/api/v1/mqtt/auth', methods=['POST'])
def mqtt_auth():
    username, password, client_id = request.form['username'], request.form['password'], request.form['clientid']
    log.info(f'Login with user:{username} - client:{client_id}')
    user = User.query.filter_by(username=username).first()
    if user and user.verify(password):
        return 'ok'
    else:
        return 'password error', 401


@app.route('/api/v1/mqtt/acl')
def mqtt_acl():
    return 'ok'
