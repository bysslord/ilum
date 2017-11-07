#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
