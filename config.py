import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'MyDB'

    SECRET_KEY = os.environ.get('SECReT_KEY') or 'idk_what_this_is'