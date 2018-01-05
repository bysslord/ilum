#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

import click
import json
import os
from util.api import NgAlertD, ServerError
from util.constant import USER_CONFIG


class Setting(dict):

    def __init__(self, namespace='default', **kwargs):
        super().__init__(**kwargs)
        self.namespace = namespace
        self.filename = os.path.join(USER_CONFIG, namespace)

    @property
    def token(self):
        return self.get('token', None)

    @token.setter
    def token(self, value):
        self['token'] = value

    def __enter__(self):
        try:
            with open(self.filename, 'r') as stream:
                self.update(json.load(stream))
        except (OSError, ValueError, FileNotFoundError):
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            if not os.path.exists(USER_CONFIG):
                os.mkdir(USER_CONFIG)
            with open(self.filename, 'w+') as stream:
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
    api.account_login()
    try:
        api.client_config(name)
    except ServerError as e:
        if e.status == 409:
            if input(f"Name {name} has already exists, want to replace? [y/n]: ").upper() == 'Y':
                client_id = api.client_config(name, replace=1)
                with Setting('auth') as setting:
                    setting[name] = {'client_id':  client_id}
            else:
                print('Configure failed!')
        else:
            raise
    else:
        print("Configure success!")


@main.command(help='Emit a message')
@click.option('--name', '-n', help='Your client name')
def emit(name):
    if not name:
        name = input("Your client name: ")
    with Setting('auth') as setting:
        s = setting.get(name)
        if not s:
            print(f'Client {name} not configure yet! Please configure at first')
        else:
            print(s)


if __name__ == '__main__':
    try:
        main()
    except ServerError as se:
        print(f'\nError-{se.status}: {se.message}')
        print(f'\nRequest id: {se.request_id}\n')
