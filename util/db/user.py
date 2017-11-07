#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from . import db, as_dict
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = 't_user'

    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    username = db.Column(db.VARCHAR, nullable=False)
    password = db.Column(db.VARCHAR, nullable=False)
    user_id = db.Column(db.CHAR, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.user_id = self._gen_user_id()

    def verify(self, password):
        return check_password_hash(self.password, password)

    def as_dict(self):
        return as_dict(self)

    @staticmethod
    def _gen_user_id():
        return f'u{str(uuid4()).replace("-", "")[0:-2]}'
