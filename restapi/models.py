from restapi import db
from sqlalchemy import ForeignKey
''' modules of user model'''


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    modefied_date = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())


class User(Base):
    ''' define user model '''

    __tablename__ = 'users'

    public_id = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(256))
    hashed_pwd = db.Column(db.String(256))
    birth = db.Column(db.DateTime)
    salt = db.Column(db.String(50))
    phone = db.Column(db.String(60))
    dpmt = db.Column(db.String(60))
    status = db.Column(db.String(60))
    img_url = db.Column(db.String(300))


class ClockInOutHistory(Base):
    ''' define check in history '''
    __tablename__ = 'clock_in_out'

    clock_in_or_out = db.Column(db.String(10))

    clock_datetime = db.Column(
        db.DateTime,
        default=db.func.current_timestamp())

    operator_id = db.Column(db.Integer, ForeignKey('users.id'))

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
