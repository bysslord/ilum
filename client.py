#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

import click
import json
import os

from util.api import NgAlertD, ServerError
from util.constant import USER_CONFIG


class Setting(dict):

    @property
    def token(self):
        return self.get('token', None)

    @token.setter
    def token(self, value):
        self['token'] = value

    def __enter__(self):
        try:
            with open(USER_CONFIG, 'r') as stream:
                self.update(json.load(stream))
        except (OSError, ValueError, FileNotFoundError):
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            with open(USER_CONFIG, 'w+') as stream:
                json.dump(self, stream)


@click.group(help='Ngalert cli app')
def main():
    pass


@main.command(help='Config ngalert')
@click.option('--username', '-u', help='Your username/email')
@click.option('--password', '-p', help='Your password')
@click.option('--name', '-n', help='Your app name')
def config(username, password, name):
    if not username:
        username = input("Your username or email: ")
    if not password:
        password = input("Your password: ")
    if not name:
        name = input("Your app name: ")
    api = NgAlertD(username, password, name)
    token = api.account_login()
    with Setting() as setting:
        setting.token = token
    print("Configure success!")


@main.command(help='Emit a message')
def emit():
    with Setting() as setting:
        if not setting.token:
            print('Please config at first')
        else:
            pass


if __name__ == '__main__':
    try:
        main()
    except ServerError as se:
        print(f'Error-{se.status}: {se.message}')
