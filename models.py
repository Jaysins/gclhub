# coding=utf-8
"""
Models
"""
# noinspection PyUnresolvedReferences

from app import db
import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    class User
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(115), unique=True)
    email = db.Column(db.String(115), unique=True)
    password = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False) 
    verified = db.Column(db.Boolean, default=False)     
    manual = db.Column(db.Boolean, default=False)
    # account = db.Column(db.relationship('Account', backref='user', lazy='dynamic'))
    # history = db.Column(db.relationship('History', backref='user', lazy='dynamic'))


class Account(db.Model):
    """
    class Account
    """
    id = db.Column(db.Integer, primary_key=True)
    plan = db.Column(db.String(100), default=None)
    sub_date = db.Column(db.DateTime, default=datetime.datetime.now())
    due_date = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    verified = db.Column(db.Boolean, default=False)
    reference = db.Column(db.String(100), default='')
    manual = db.Column(db.Boolean, default=False)


class History(db.Model):
    """
    class History
    """
    id = db.Column(db.Integer, primary_key=True)
    plan = db.Column(db.String(100), default=None)
    sub_date = db.Column(db.DateTime, default=datetime.datetime.now())
    due_date = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
