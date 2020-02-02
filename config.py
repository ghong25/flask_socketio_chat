import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-mystery'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://ghong25:p3KstlK7OwZ66LNRHcGA@database-1.c5aqdxmdgobi.us-east-1.rds.amazonaws.com:5432/database-1"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
