#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'
from coloredlogs import install
import logging


fmt = '%(asctime)s %(name)10s(%(process)5d) %(threadName)s' \
      '%(levelname)7s %(filename)16s:%(lineno)3s %(message)s'
install(fmt=fmt)

log = logging.getLogger('ngalertd')

trace = logging.getLogger('trace')

logging.getLogger('werkzeug').setLevel(logging.ERROR)

logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
