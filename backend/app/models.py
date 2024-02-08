#!/usr/bin/python3
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime
from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(264))

    expenses: so.WriteOnlyMapped['Expense'] = so.relationship(
        back_populates='author')
    income: so.WriteOnlyMapped['Income'] = so.relationship(
        back_populates='author')
    budget: so.WriteOnlyMapped['Budget'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return 'User {}'.format(self.username)

class Expense(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    amount: so.Mapped[float] = so.mapped_column(sa.Float)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.utcnow())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='expenses')

    def __repr__(self):
        return 'Expense: {}, {}, {}'.format(self.description, self.amount, self.timestamp)
    
class Income(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    amount: so.Mapped[float] = so.mapped_column(sa.Float)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.utcnow())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='income')

    def __repr__(self) -> str:
        return 'Income: {}, {}, {}'.format(self.description, self.amount, self.timestamp)
    

class Budget(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    category: so.Mapped[str] = so.mapped_column(sa.String(255))
    asigned: so.Mapped[float] = so.mapped_column(sa.Float)
    activity: so.Mapped[float] = so.mapped_column(sa.Float)
    available: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, default=0.0 ,nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.utcnow())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='budget')


    def __repr__(self) -> str:
        return 'Budget Set: {}: {}, {}, {} set at {}'.format(self.category, self.asigned, self.activity, self.timestamp)


def format_budget(budget):
    return {
        "id": budget.id,
        "category": budget.category,
        "asigned": budget.asigned,
        "activity": budget.activity,
        "available": budget.available,
        "timestamp": budget.timestamp.strftime("%y-%b-%a %H:%M")
    }