# coding: utf-8
from sqlalchemy import Column, Integer, Numeric, Table, Text
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)


class Channel(db.Model):
    __tablename__ = 'channel'

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.Integer)
    strategy = db.Column(db.Integer)
    status = db.Column(db.Text)
    reporting = db.Column(db.Integer)
    count_success = db.Column(db.Integer)
    name = db.Column(db.Text, nullable=False)
    channel = db.Column(db.Text, nullable=False)
    count_fail = db.Column(db.Integer)


class Email(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    recovery_email = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Text)
    email = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Numeric)


class FakeUser(db.Model):
    __tablename__ = 'fake_user'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.Text)
    gender = db.Column(db.Text)
    state = db.Column(db.Text)
    name = db.Column(db.Integer)
    address_1 = db.Column(db.Text)
    address_2 = db.Column(db.Text)
    city = db.Column(db.Text)
    zip_code = db.Column(db.Text)
    phone = db.Column(db.Text)


class Mac(db.Model):
    __tablename__ = 'mac'

    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.Text)
    created_date = db.Column(db.Integer)


class Strategy(db.Model):
    __tablename__ = 'strategy'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    note = db.Column(db.Text)
    issue = db.Column(db.Text)
    sub_issue = db.Column(db.Text)
    create_date = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.Text)
    fullname = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.Integer)
    role = db.Column(db.Text)


class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text)
    count_success = db.Column(db.Integer)
    count_fail = db.Column(db.Integer)
    first_time = db.Column(db.Text)
    second_time = db.Column(db.Text)


class View(db.Model):
    __tablename__ = 'views'

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.Integer)
    count = db.Column(db.Integer)
    keyword = db.Column(db.Text)
    status = db.Column(db.Text)
    channel = db.Column(db.Text, nullable=False)
