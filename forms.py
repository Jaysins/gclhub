# coding=utf-8

"""
Forms package
"""

from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """
    Register
    """
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='invalid email'), Length(max=50)])
    # number = StringField('Number', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='password DONT match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
    """
    LoginForm
    """
    name = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=90)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
