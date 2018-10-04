# coding=utf-8

"""
Forms package
"""

from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """
    Register
    """
    name = StringField('Name', validators=[InputRequired(), Length(min=4)])
    email = StringField('Email', validators=[InputRequired(), Email(message='invalid email')])
    # number = StringField('Number', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), DataRequired(), EqualTo('confirm', message='Passwords Dont Match'), Length(min=8, max=80)])
    confirm = PasswordField('Repeat Password')


class AddNewForm(FlaskForm):
    """
    AddNew
    """
    name = StringField('Name', validators=[InputRequired(), Length(min=4)])
    email = StringField('Email', validators=[InputRequired(), Email(message='invalid email')])
    hours = IntegerField('Hours', validators=[InputRequired()])
    date = DateField('Start Date', format='%Y-%m-%d')
    space = StringField('Space', validators=[InputRequired(), Length(min=3)])
        

class LoginForm(FlaskForm):
    """
    LoginForm
    """
    name = StringField('Username', validators=[
                           InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8)])


class AdminLoginForm(FlaskForm):
    """
    LoginForm
    """
    name = StringField('Username', validators=[
                           InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8)])
