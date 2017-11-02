#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from web.view import *
from util.db import db
from util import configure


if __name__ == '__main__':
    db.init_app(app)
    app.run(
        configure.GLOBAL.get('host', '127.0.0.1'),
        int(configure.GLOBAL.get('port', 9757)),
        debug=True if configure.GLOBAL.get('debug', '1') == '1' else False
    )

