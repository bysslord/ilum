#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

from .. import app, Required, Optional, get_params, g, BaseError
from web import auth
from util.db.client import Client, db
from util.db.user import User


@app.route('/api/v1/client/config', methods=['GET', 'POST'])
@auth.token
def client_info():
    """
    :return:
    """
    args = get_params(
        (
            ('name', str, Required, None),
            ('replace', int, Optional, 0)
        ),
    )

    user = g.user   # type: User

    name = args.get('name')
    replace = args.get('replace')

    client = Client.query.filter_by(owner=user.user_id, name=name).first()   # type: Client
    if not client:
        client = Client(name, user.user_id)
        db.session.add(client)
    else:
        if not replace:
            raise BaseError(f"Name {name} has already exists.", 409)
        else:
            client.name = name
            client.client_id = client.gen_client_id()

    db.session.commit()
    return client.client_id
