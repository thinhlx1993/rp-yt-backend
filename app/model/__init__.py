# coding: utf-8
import time
from sqlalchemy import Column, Integer, Numeric, Table, Text
from app.extensions import db


class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, name, status, created_date):
        self.name = name
        self.status = status
        self.created_date = created_date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


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

    def __init__(self, strategy, status, reporting, count_success, count_fail, name, channel):
        self.create_date = int(time.time())
        self.strategy = strategy
        self.status = status
        self.reporting = reporting
        self.count_success = count_success
        self.count_fail = count_fail
        self.name = name
        self.channel = channel

    def json(self):
        return dict(
            id=self.id,
            strategy=self.strategy,
            create_date=self.create_date,
            status=self.status,
            reporting=self.reporting,
            count_success=self.count_success,
            count_fail=self.count_fail,
            name=self.name,
            channel=self.channel,
        )

    @classmethod
    def get_channels(cls, search, page, page_size):
        if search != '':
            data = cls.query.filter(cls.name.contains(search)).paginate(
                page, page_size, error_out=False)
            totals = cls.query.filter(cls.name.contains(search)).count()
        else:
            data = cls.query.filter().paginate(page, page_size, error_out=False)
            totals = cls.query.filter().count()
        return data, totals

    @classmethod
    def find_exist(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter(cls.id == _id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Email(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    recovery_email = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Text)
    email = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer)

    def __init__(self, password, recovery_email, status, date, email, phone):
        self.password = password
        self.recovery_email = recovery_email
        self.status = status
        self.date = date
        self.email = email
        self.phone = phone

    def json(self):
        return {"id": self.id, 'password': self.password, 'recovery_email': self.recovery_email, 'status': self.status,
                'date': self.date, 'email': self.email, 'phone': self.phone}

    @classmethod
    def find_by_keyword(cls, keyword, page=1, page_size=10):
        if keyword != '':
            data = cls.query.filter(cls.email.contains(keyword)).paginate(
                page, page_size, error_out=False)
        else:
            data = cls.query.filter().paginate(page, page_size, error_out=False)
        totals = cls.query.filter_by().count()
        return data, totals

    @classmethod
    def find_by_id(cls, email_id):
        return cls.query.filter_by(id=email_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Mac(db.Model):
    __tablename__ = 'mac'

    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.Text)
    created_date = db.Column(db.Integer)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Strategy(db.Model):
    __tablename__ = 'strategy'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    note = db.Column(db.Text)
    issue = db.Column(db.Text)
    sub_issue = db.Column(db.Text)
    create_date = db.Column(db.Integer)

    def __init__(self, name, note, issue, sub_issue, create_date):
        self.name = name
        self.note = note
        self.issue = issue
        self.sub_issue = sub_issue
        self.create_date = create_date

    def json(self):
        return {"id": self.id, 'name': self.name, 'note': self.note, 'issue': self.issue,
                'sub_issue': self.sub_issue, 'create_date': self.create_date}

    @classmethod
    def find_by_keyword(cls, keyword, page=1, page_size=10):
        if keyword != '':
            data = cls.query.filter(cls.name.contains(keyword)).paginate(
                page, page_size, error_out=False)
        else:
            data = cls.query.filter().paginate(page, page_size, error_out=False)
        totals = cls.query.filter_by().count()
        return data, totals

    @classmethod
    def find_by_id(cls, strategy_id):
        return cls.query.filter_by(id=strategy_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by().all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


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

    def __init__(self, username, address, phone, fullname, password, create_date, role):
        self.username = username
        self.address = address
        self.phone = phone
        self.fullname = fullname
        self.password = password
        self.create_date = create_date
        self.role = role

    def json(self):
        return {"id": self.id, 'username': self.username, 'address': self.address, 'phone': self.phone,
                'create_date': self.create_date, 'role': self.role, 'fullname': self.fullname}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_by_keyword(cls, keyword, page=1, page_size=10):
        if keyword != '':
            data = cls.query.filter(cls.username.contains(keyword)).paginate(
                page, page_size, error_out=False)
        else:
            data = cls.query.filter().paginate(page, page_size, error_out=False)
        totals = cls.query.filter_by().count()
        return data, totals

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class View(db.Model):
    __tablename__ = 'views'

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.Integer)
    count = db.Column(db.Integer)
    keyword = db.Column(db.Text)
    status = db.Column(db.Text)
    channel = db.Column(db.Text, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()