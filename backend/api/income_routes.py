from flask import Blueprint, abort
from flask_cors import CORS
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import User, Income
from api.schemas import IncomeSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas import DateTimePaginationSchema

incomes = Blueprint('incomes', __name__)
CORS(incomes)
income_schema = IncomeSchema()
incomes_schema = IncomeSchema(many=True)
update_income_schema = IncomeSchema(partial=True)


@incomes.route('/income', methods= ['POST'])
@authenticate(token_auth)
@body(income_schema)
@response(income_schema, 201)
def new(args):
    """Create a new income"""
    user = token_auth.current_user()
    income = income(author=user, **args)
    db.session.add(income)
    db.session.commit()
    return income


@incomes.route('/incomes/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(income_schema)
@other_responses({404: 'income not found'})
def get(id):
    """Retrieve a income by id"""
    return db.session.get(Income, id) or abort(404)


@incomes.route('/incomes', methods=['GET'])
@authenticate(token_auth)
@paginated_response(incomes_schema, order_by=Income.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all():
    """Retrieve all incomes"""
    return Income.select()


@incomes.route('/users/<int:id>/incomes', methods=['GET'])
@authenticate(token_auth)
@paginated_response(incomes_schema, order_by=Income.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'User not found'})
def user_all(id):
    """Retrieve all incomes from a user"""
    user = db.session.get(User, id) or abort(404)
    return user.incomes.select()


@incomes.route('/incomes/<int:id>', methods=['PUT'])
@authenticate(token_auth)
@body(update_income_schema)
@response(income_schema)
@other_responses({403: 'Not allowed to edit this income',
                  404: 'income not found'})
def put(data, id):
    """Edit an income"""
    income = db.session.get(Income, id) or abort(404)
    if income.author != token_auth.current_user():
        abort(403)
    income.update(data)
    db.session.commit()
    return income


@incomes.route('/incomes/<int:id>', methods=['DELETE'])
@authenticate(token_auth)
@other_responses({403: 'Not allowed to delete the income'})
def delete(id):
    """Delete an income"""
    income = db.session.get(Income, id) or abort(404)
    if income.author != token_auth.current_user():
        abort(403)
    db.session.delete(income)
    db.session.commit()
    return '', 204
