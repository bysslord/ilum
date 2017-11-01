#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from .. import app


@app.route('/')
def home():
    return 'hello'
