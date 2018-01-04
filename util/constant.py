#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

import os

HOME = os.path.dirname(os.path.dirname(__file__))
CONF_FILE = os.path.join(HOME, 'conf', 'app.ini')
USER_CONFIG = os.path.join(os.path.expanduser('~'), '.ngalert')
