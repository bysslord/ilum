#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from flask import Flask, request
from util.configure import DB
from util.logger import log, trace

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB.get('url')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a#EDRTE%'


class Required(object):
    val = 1


class Optional(object):
    val = 2


class BaseError(Exception):
    status_code = 400

    def __init__(self, message=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        self.message = message

    def __str__(self):
        return self.message


class ArgumentMissingError(BaseError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Argument {self.name} was required.'


class ArgumentCastError(BaseError):
    def __init__(self, name, cast, exc):
        self.name = name
        self.cast = cast
        self.exc = exc

    def __str__(self):
        return f'Argument {self.name} is not casted by {self.cast} because {self.exc}'


def get_params(params: tuple, data=None) -> dict:
    if not data:
        data = request.args
    res = {}
    for name, cast, attr, default in params:
        value = data.get(name)
        if not value:
            if attr is Required:
                raise ArgumentMissingError(name)
            value = default
        if callable(cast):
            try:
                value = cast(value)
            except Exception as e:
                raise ArgumentCastError(name, cast, e)
        res[name] = value
    return res


@app.errorhandler(BaseError)
def handler(exception):
    return str(exception), exception.status_code


@app.errorhandler(Exception)
def un_handler(exception):
    from traceback import format_exc
    log.error(f'Error {exception}')
    trace.error(format_exc())
    return 'Internal Server Error', 500
