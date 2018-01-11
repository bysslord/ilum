#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from flask import Flask, request, jsonify, g, make_response, Response
from util.configure import DB
from util.logger import log, trace

from traceback import format_exc
from threading import currentThread
from uuid import uuid4
import time

app = Flask(__name__, template_folder='public/templates', static_folder='public/static')

app.config['SQLALCHEMY_DATABASE_URI'] = DB.get('url')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a#EDRTE%'

# app.session_interface = RedisSessionInterface(prefix="NGALERTD:SESSION:")


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
        self.message = str(self)

    def __str__(self):
        return f'Argument {self.name} was required.'


class ArgumentCastError(BaseError):
    def __init__(self, name, cast, exc):
        self.name = name
        self.cast = cast
        self.exc = exc
        self.message = str(self)

    def __str__(self):
        return f'Argument {self.name} is not casted by {self.cast} because {self.exc}'


def get_params(params: tuple, data=None) -> dict:
    """
    :param params: sdf
    :param data:
    :return:
    """
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


_max_rule = 0


def route(rule, **options):

    def decorator(f):

        global _max_rule
        _max_rule = max(_max_rule, len(rule))

        def wrapper(*args, **kwargs):
            """
            Make endpoint's result to a json object
            :param args:
            :param kwargs:
            :return:
            """

            request_id = str(uuid4())
            path = request.path.rjust(_max_rule)
            method = str(request.method).rjust(6)
            currentThread().name = f'{request_id}:{method}:{path}:'
            start = time.time()

            g.res = {
                'request_id': request_id,
                'result': None,
                'status': 200,
                'error': None
            }

            try:
                response = f(*args, **kwargs)
                if not request.path.startswith('/api'):
                    return make_response(response, {'X-Request-ID': request_id})
                g.res.update(result=response)
            except BaseError as be:
                log.error(f"{str(be)}")
                g.res.update(
                    status=be.status_code,
                    error=be.message
                )
            finally:
                elapse = (time.time() - start) * 1000
                log.info(f"Request done. elapse(ms): {elapse:5f}, status: {g.res['status']}")

            return jsonify(g.res)

        endpoint = options.pop('endpoint', f.__name__)
        log.info(f'Route url {str(rule)} -> {f}')
        app.add_url_rule(rule, endpoint, wrapper, **options)

        return wrapper

    return decorator


app.route = route


@app.after_request
def no_cache(response: Response):
    response.cache_control.no_cache = True
    return response


@app.errorhandler(Exception)
def handle(e):
    trace.error(format_exc())
    log.error(f"Un handler exception: {e}")
    g.res.update(status=500, error='Internal server error', result=None)
    return jsonify(g.res)
