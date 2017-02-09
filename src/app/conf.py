# -*- coding: utf-8 -*-
#


class Shared:
    SQLALCHEMY_POOL_SIZE = 450
    SQLALCHEMY_POOL_TIMEOUT = 5400
    SQLALCHEMY_POOL_RECYCLE = 7200
    SQLALCHEMY_ECHO = True
    DEBUG = True


class Prod(Shared):
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_DATABASE_URI = 'mysql://127.0.0.1/whiteboard'
    SQLALCHEMY_ECHO = True


class Dev(Shared):

    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_DATABASE_URI = 'mysql://127.0.0.1/whiteboard'
    SQLALCHEMY_ECHO = True