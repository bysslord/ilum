#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from . import db, as_dict, BaseQuery
from uuid import uuid4


class Client(db.Model):

    query: BaseQuery

    __tablename__ = 't_client'

    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    owner = db.Column(db.VARCHAR, nullable=False)
    client_id = db.Column(db.CHAR, nullable=False)

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.client_id = self.gen_client_id()

    def as_dict(self):
        return as_dict(self)

    @staticmethod
    def gen_client_id():
        return f'c{str(uuid4()).replace("-", "")[0:-2]}'
