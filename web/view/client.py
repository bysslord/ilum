#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from .. import app, Required, get_params, session
from util.db.client import Client


@app.route('/client/info', methods=['GET'])
def client_info():
    args = get_params(
        (
            ('token', str, Required, None),
        ),
    )

    print(session.get('token'))

    session['token'] = 'test'

    return args
