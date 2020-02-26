from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    # mixin provides default implementations for the methods that Flask-Login expects user objects to have.
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}'


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    from_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    chatroom = db.Column(db.String(60))

    def __repr__(self):
        return f'<Message {self.message}'

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:zeKaXHNnj3FpnGJj@database-1.c5aqdxmdgobi.us-east-1.rds.amazonaws.com:5432")
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()
#q = eng.execute("select column_name, data_type from information_schema.columns where table_name = 'message'")
#engine.execute("select * from public.user")
session.execute("delete from public.message where from_user = 8")
#print(q.fetchall())
"""
