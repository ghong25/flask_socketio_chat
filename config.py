import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-mystery'
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:zeKaXHNnj3FpnGJj@database-1.c5aqdxmdgobi.us-east-1.rds.amazonaws.com:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
