#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'
from coloredlogs import install
import logging


fmt = '%(asctime)s %(name)10s(%(process)5d) ' \
      '%(levelname)7s %(filename)16s:%(lineno)3s %(message)s'
install(fmt=fmt)

log = logging.getLogger('ngalertd')

trace = logging.getLogger('trace')
