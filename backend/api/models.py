#!/usr/bin/python3
from datetime import datetime, timedelta
from hashlib import md5
import secrets
from time import time
from typing import Optional

from flask import current_app, url_for
import jwt
import sqlalchemy as sa
from sqlalchemy import orm as so
from sqlalchemy.orm import configure_mappers
from werkzeug.security import generate_password_hash, check_password_hash

from api.app import db


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Token(db.Model):
    __tablename__ = 'tokens'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    access_token: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    access_expiration: so.Mapped[datetime]
    refresh_token: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    refresh_expiration: so.Mapped[datetime]
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('users.id'), index=True)

    user: so.Mapped['User'] = so.relationship(back_populates='tokens')

    @property
    def access_token_jwt(self):
        return jwt.encode({'token': self.access_token},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256')

    def generate(self):
        self.access_token = secrets.token_urlsafe()
        self.access_expiration = datetime.utcnow() + \
            timedelta(minutes=current_app.config['ACCESS_TOKEN_MINUTES'])
        self.refresh_token = secrets.token_urlsafe()
        self.refresh_expiration = datetime.utcnow() + \
            timedelta(days=current_app.config['REFRESH_TOKEN_DAYS'])

    def expire(self, delay=None):
        if delay is None:
            # 10 second delay to allow simultaneous requests
            delay = 10 if not current_app.testing else 0
        self.access_expiration = datetime.utcnow() + timedelta(seconds=delay)
        self.refresh_expiration = datetime.utcnow() + timedelta(seconds=delay)

    @staticmethod
    def clean():
        """Remove any tokens that have been expired for more than a day."""
        yesterday = datetime.utcnow() - timedelta(days=1)
        db.session.execute(Token.delete().where(
            Token.refresh_expiration < yesterday))

    @staticmethod
    def from_jwt(access_token_jwt):
        access_token = None
        try:
            access_token = jwt.decode(access_token_jwt,
                                      current_app.config['SECRET_KEY'],
                                      algorithms=['HS256'])['token']
            return db.session.scalar(Token.select().filter_by(
                access_token=access_token))
        except jwt.PyJWTError:
            pass


class User(Updateable, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    first_seen: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
    last_seen: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)

    tokens: so.WriteOnlyMapped['Token'] = so.relationship(
        back_populates='user')
    expenses: so.WriteOnlyMapped['Expense'] = so.relationship(
        back_populates='author', lazy='dynamic')
    incomes: so.WriteOnlyMapped['Income'] = so.relationship(
        back_populates='author', lazy='dynamic')
    budgets: so.WriteOnlyMapped['Budget'] = so.relationship(
        back_populates='author', lazy='dynamic')
  
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def url(self):
        return url_for('users.get', id=self.id)

    @property
    def has_password(self):
        return self.password_hash is not None

    @property
    def avatar_url(self):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if self.password_hash:
            return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()

    def generate_auth_token(self):
        token = Token(user=self)
        token.generate()
        return token

    @staticmethod
    def verify_access_token(access_token_jwt, refresh_token=None):
        token = Token.from_jwt(access_token_jwt)
        if token:
            if token.access_expiration > datetime.utcnow():
                token.user.ping()
                db.session.commit()
                return token.user

    @staticmethod
    def verify_refresh_token(refresh_token, access_token_jwt):
        token = Token.from_jwt(access_token_jwt)
        if token and token.refresh_token == refresh_token:
            if token.refresh_expiration > datetime.utcnow():
                return token

            # someone tried to refresh with an expired token
            # revoke all tokens from this user as a precaution
            token.user.revoke_all()
            db.session.commit()

    def revoke_all(self):
        db.session.execute(Token.delete().where(Token.user == self))

    def generate_reset_token(self):
        return jwt.encode(
            {
                'exp': time() + current_app.config['RESET_TOKEN_MINUTES'] * 60,
                'reset_email': self.email,
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_token(reset_token):
        try:
            data = jwt.decode(reset_token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except jwt.PyJWTError:
            return
        return db.session.scalar(User.select().filter_by(
            email=data['reset_email']))


class Expense(Updateable, db.Model):
    __tablename__ = 'expenses'


    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    amount: so.Mapped[float] = so.mapped_column(sa.Float)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.utcnow())
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='expenses')

    def __repr__(self):
        return 'Expense: {}, {} '.format(self.description, self.amount)
    
    @property
    def url(self):
        return url_for('expenses.get', id=self.id)
    

class Income(Updateable, db.Model):
    __tablename__ = 'incomes'


    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    amount: so.Mapped[float] = so.mapped_column(sa.Float)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.utcnow())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='incomes')

    def __repr__(self) -> str:
        return 'Incomes: {}, {} '.format(self.description, self.amount)
    
    @property
    def url(self):
        return url_for('incomes.get', id=self.id)


class Budget(Updateable, db.Model):
    __tablename__ = 'budgets'


    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    category: so.Mapped[str] = so.mapped_column(sa.String(255))
    assigned: so.Mapped[float] = so.mapped_column(sa.Float)
    activity: so.Mapped[float] = so.mapped_column(sa.Float)
    available: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, default=0.0 ,nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.utcnow())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='budgets')


    def __repr__(self) -> str:
        return 'Budgets Set: {}: {}, {}, {} set at {}'.format(self.category, self.asigned, self.activity, self.timestamp)
    
    @property
    def url(self):
        return url_for('budgets.get', id=self.id)
    
configure_mappers()
