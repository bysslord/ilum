#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from . import db
from uuid import uuid4
from hashlib import md5


class User(db.Model):

    __tablename__ = 't_user'

    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    username = db.Column(db.VARCHAR, nullable=False)
    password = db.Column(db.VARCHAR, nullable=False)
    user_id = db.Column(db.CHAR, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = self._encrypt_pwd(password)
        self.user_id = self._gen_user_id()

    def verify(self, password):
        return self._encrypt_pwd(password) == self.password

    @staticmethod
    def _gen_user_id():
        return f'u{str(uuid4()).replace("-", "")[0:-2]}'

    @staticmethod
    def _encrypt_pwd(pwd):
        return md5(md5(str(pwd).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
