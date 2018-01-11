#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from flask_socketio import SocketIO
from flask import request


socketio = SocketIO()


@socketio.on('system')
def system(message):
    print(message)
    print(request.path)
