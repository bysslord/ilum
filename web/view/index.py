#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from .. import app
from flask import render_template


@app.route('/')
def home():
    return render_template('index.html')
