#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from web.view import *
from web.socketio import socketio
from util.db import db
from util import configure
from util.logger import log


if __name__ == '__main__':
    db.init_app(app)
    socketio.init_app(app)
    host, port, debug = configure.GLOBAL.get('host', '127.0.0.1'), \
        int(configure.GLOBAL.get('port', 9757)), \
        True if configure.GLOBAL.get('debug', '1') == '1' else False

    log.info(f'Start server at {host}:{port}, debug:{debug}')
    socketio.run(
        app, host=host, port=port, debug=debug
    )

