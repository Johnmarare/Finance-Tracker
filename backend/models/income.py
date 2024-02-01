#!/usr/bin/python3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))


    def __repr__(self):
        return f"Income: {self.amount}, {self.description}, {self.date}"
    
    def __init__(self, description, amount, date=None):
        self.description = description
        self.amount = amount
        self.date = date if date else datetime.utcnow()

    def format_income(income):
        return {
            "description": income.description,
            "amount": income.amount,
            "created_at": income.date,
            "id": income.id
        }