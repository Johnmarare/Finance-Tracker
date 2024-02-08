from flask import request, jsonify
import sqlalchemy as sa
from app import app, db

from app.models import User, Expense


@app.route('/')
@app.route('/index')
def index():
    return "Hello world"

@app.route('/expense', methods= ['POST'])
def create_expense():
    """Create an expense"""
    try:
        data = request.json
        description = data.get("description")
        amount = data.get("amount")
        user_id = data.get("user_id")

        
        expense = Expense(description=description, amount=amount, user_id=user_id)
        db.session.add(expense)
        db.session.commit()

        return jsonify({"mesage": "Expense created succesfully"})
    except Exception as e:
        print(f"Error creating expense: {e}")
        return jsonify({"error": "Error creating expense"})

@app.route('/expense', methods=['GET'])
def get_expense():
    """get expense for user"""
    try:
        expenses = Expense.query.all()
        # convert expenses to a list of dicts for json response
        expense_list = [{"id": expense.id, "description": expense.description, "amount": expense.amount} for expense in expenses]
        return jsonify({"expenses": expense_list})
    except Exception as e:
        print (f"Error getting expenses: {e}")
        return jsonify({"error": "Error getting expenses"})
    
@app.route('/expense/<int:expense_id>', methods=['GET'])
def get_exp(expense_id):
    """retrieve expense uniquely by ID"""
    try:
        expense = Expense.query.get(expense_id)

        if expense:
            # Convert expense to a dictionary ffor json response
            expense_data = {"id": expense.id, "description": expense.description, "amount": expense.amount}
            return jsonify({"expense": expense_data})
        else:
            return jsonify({"error": "Expense not found"}), 404
    except Exception as e:
        print(f"Error getting expense: {e}")
        return jsonify({"error": "Error getting expense"}) 
@app.route('/expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Deletes a specific expense"""
    try:
        expense = Expense.query.get(expense_id)

        if expense:
            db.session.delete(expense)
            db.session.commit()
            return jsonify({"message": "Expense deleted succesfully"})
        else:
            return jsonify({"error": "Expense not founf"}), 404
    
    except Exception as e:
        print(f"Error deleting expense: {e}")
        return jsonify({"error": f"Error deleting expense: {str(e)}"})


@app.route('/expense/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update the expense table by ID"""
    try:
        expense = Expense.query.get(expense_id)

        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        # Update expense attributes
        expense.description = request.json["description"]
        expense.amount = request.json["amount"]

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Expense updated successfully"})
    except Exception as e:
        print(f"Error updating expense: {e}")
        db.session.rollback()
        return jsonify({"error": f"Error updating expense: {str(e)}"}), 500
