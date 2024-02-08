from flask import request, jsonify
import sqlalchemy as sa
from app import app, db

from app.models import User, Income



@app.route('/income', methods= ['POST'])
def create_income():
    """Create an income"""
    try:
        data = request.json
        description = data.get("description")
        amount = data.get("description")
        user_id = data.get("user_id")
        
        income = Income(description=description, amount=amount, user_id=user_id)
        db.session.add(income)
        db.session.commit()

        return jsonify({"mesage": "Income created succesfully"})
    except Exception as e:
        print(f"Error creating income: {e}")
        return jsonify({"error": "Error creating income"})

@app.route('/income', methods=['GET'])
def get_income():
    """get income for user"""
    try:
        incomes = Income.query.all()
        # convert incomes to a list of dicts for json response
        income_list = [{"id": income.id, "description": income.description, "amount": income.amount} for income in incomes]
        return jsonify({"incomes": income_list})
    except Exception as e:
        print (f"Error getting incomes: {e}")
        return jsonify({"error": "Error getting incomes"})
    
@app.route('/income/<int:income_id>', methods=['GET'])
def get_income_by_id(income_id):
    """retrieve income uniquely by ID"""
    try:
        income = Income.query.get(income_id)

        if income:
            # Convert income to a dictionary ffor json response
            income_data = {"id": income.id, "description": income.description, "amount": income.amount}
            return jsonify({"income": income_data})
        else:
            return jsonify({"error": "Income not found"}), 404
    except Exception as e:
        print(f"Error getting income: {e}")
        return jsonify({"error": "Error getting income"}) 
@app.route('/income/<int:income_id>', methods=['DELETE'])
def delete_income(income_id):
    """Deletes a specific income"""
    try:
        income = Income.query.get(income_id)

        if income:
            db.session.delete(income)
            db.session.commit()
            return jsonify({"message": "Income deleted succesfully"})
        else:
            return jsonify({"error": "Income not founf"}), 404
    
    except Exception as e:
        print(f"Error deleting income: {e}")
        return jsonify({"error": f"Error deleting income: {str(e)}"})


@app.route('/income/<int:income_id>', methods=['PUT'])
def update_income(income_id):
    """Update the income table by ID"""
    try:
        income = Income.query.get(income_id)

        if not income:
            return jsonify({"error": "Income not found"}), 404

        # Update income attributes
        income.description = request.json["description"]
        income.amount = request.json["amount"]

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Income updated successfully"})
    except Exception as e:
        print(f"Error updating income: {e}")
        db.session.rollback()
        return jsonify({"error": f"Error updating income: {str(e)}"}), 500
