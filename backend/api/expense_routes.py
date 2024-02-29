from flask import Blueprint, abort
from flask_cors import CORS
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import User, Expense
from api.schemas import ExpenseSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas import DateTimePaginationSchema

expenses = Blueprint('expenses', __name__)
CORS(expenses)
expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)
update_expense_schema = ExpenseSchema(partial=True)


@expenses.route('/expense', methods= ['POST'])
@authenticate(token_auth)
@body(expense_schema)
@response(expense_schema, 201)
def new(args):
    """Create a new expense"""
    user = token_auth.current_user()
    expense = expense(author=user, **args)
    db.session.add(expense)
    db.session.commit()
    return expense


@expenses.route('/expenses/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(expense_schema)
@other_responses({404: 'expense not found'})
def get(id):
    """Retrieve a expense by id"""
    return db.session.get(Expense, id) or abort(404)


@expenses.route('/expenses', methods=['GET'])
@authenticate(token_auth)
@paginated_response(expenses_schema, order_by=Expense.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all():
    """Retrieve all expenses"""
    return Expense.select()


@expenses.route('/users/<int:id>/expenses', methods=['GET'])
@authenticate(token_auth)
@paginated_response(expenses_schema, order_by=Expense.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'User not found'})
def user_all(id):
    """Retrieve all expenses from a user"""
    user = db.session.get(User, id) or abort(404)
    return user.expenses.select()


@expenses.route('/expenses/<int:id>', methods=['PUT'])
@authenticate(token_auth)
@body(update_expense_schema)
@response(expense_schema)
@other_responses({403: 'Not allowed to edit this expense',
                  404: 'expense not found'})
def put(data, id):
    """Edit a expense"""
    expense = db.session.get(Expense, id) or abort(404)
    if expense.author != token_auth.current_user():
        abort(403)
    expense.update(data)
    db.session.commit()
    return expense


@expenses.route('/expenses/<int:id>', methods=['DELETE'])
@authenticate(token_auth)
@other_responses({403: 'Not allowed to delete the expense'})
def delete(id):
    """Delete an expense"""
    expense = db.session.get(Expense, id) or abort(404)
    if expense.author != token_auth.current_user():
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    return '', 204
