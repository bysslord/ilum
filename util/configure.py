#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

import os
from . import constant
from configparser import RawConfigParser

if not os.path.exists(constant.CONF_FILE):
    raise Exception(f'Conf file {constant.CONF_FILE} not exists.')

_config = RawConfigParser()
_config.read([constant.CONF_FILE, ])

GLOBAL = dict(_config.items('global'))
DB = dict(_config.items('db'))
