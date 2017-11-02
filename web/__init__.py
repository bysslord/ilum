#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from flask import Flask
from util.configure import DB

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB.get('url')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


