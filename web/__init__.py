#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from flask import Flask, request, jsonify, g
from util.configure import DB
from util.logger import log, trace

from traceback import format_exc
from threading import currentThread
from uuid import uuid4

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


"""
Response type:
    - success: 200 ok json
    - failed: 200 ok json
    - unexpected: other code html
    
   
A decorator tip:
 
@some
def a():
    pass
    
equals to:

def a():
    pass
a = some(a)    

"""


def route(rule, **options):

    def decorator(f):

        def wrapper(*args, **kwargs):
            """
            Make endpoint's result to a json object
            :param args:
            :param kwargs:
            :return:
            """

            request_id = str(uuid4())
            path = request.path
            method = str(request.method).rjust(6)
            currentThread().name = f'{request_id}:{method}:{path}:'

            g.res = {
                'request_id': request_id,
                'result': None,
                'status': 200,
                'error': None
            }

            try:
                g.res.update(result=f(*args, **kwargs))
            except BaseError as be:
                log.warn(f"Warning: {str(be)}")
                g.res.update(
                    status=be.status_code,
                    error=be.message
                )

            return jsonify(g.res)

        endpoint = options.pop('endpoint', f.__name__)
        app.add_url_rule(rule, endpoint, wrapper, **options)

        return wrapper

    return decorator


app.route = route


@app.errorhandler(Exception)
def handle(e):
    trace.error(format_exc())
    log.error(f"Un handler exception: {e}")
    g.res.update(status=500, error='Internal server error', result=None)
    return jsonify(g.res)
