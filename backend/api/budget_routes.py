from flask import Blueprint, abort
from flask_cors import CORS
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import User, Budget
from api.schemas import BudgetSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas import DateTimePaginationSchema

budgets = Blueprint('budgets', __name__)
CORS(budgets)
budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)
update_budget_schema = BudgetSchema(partial=True)


@budgets.route('/budget', methods= ['POST'])
@authenticate(token_auth)
@body(budget_schema)
@response(budget_schema, 201)
def new(args):
    """Create a new budget"""
    user = token_auth.current_user()
    budget = budget(author=user, **args)
    db.session.add(budget)
    db.session.commit()
    return budget


@budgets.route('/budgets/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(budget_schema)
@other_responses({404: 'budget not found'})
def get(id):
    """Retrieve a budget by id"""
    return db.session.get(Budget, id) or abort(404)


@budgets.route('/budgets', methods=['GET'])
@authenticate(token_auth)
@paginated_response(budgets_schema, order_by=Budget.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all():
    """Retrieve all budgets"""
    return Budget.select()


@budgets.route('/users/<int:id>/budgets', methods=['GET'])
@authenticate(token_auth)
@paginated_response(budgets_schema, order_by=Budget.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'User not found'})
def user_all(id):
    """Retrieve all budgets from a user"""
    user = db.session.get(User, id) or abort(404)
    return user.budgets.select()


@budgets.route('/budgets/<int:id>', methods=['PUT'])
@authenticate(token_auth)
@body(update_budget_schema)
@response(budget_schema)
@other_responses({403: 'Not allowed to edit this budget',
                  404: 'budget not found'})
def put(data, id):
    """Edit a budget"""
    budget = db.session.get(Budget, id) or abort(404)
    if budget.author != token_auth.current_user():
        abort(403)
    budget.update(data)
    db.session.commit()
    return budget


@budgets.route('/budgets/<int:id>', methods=['DELETE'])
@authenticate(token_auth)
@other_responses({403: 'Not allowed to delete the budget'})
def delete(id):
    """Delete a budget"""
    budget = db.session.get(Budget, id) or abort(404)
    if budget.author != token_auth.current_user():
        abort(403)
    db.session.delete(budget)
    db.session.commit()
    return '', 204
