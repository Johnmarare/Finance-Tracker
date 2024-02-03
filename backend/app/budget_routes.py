from flask import request, jsonify
import sqlalchemy as sa
from app import app, db

from app.models import User, Budget, format_budget

@app.route('/budget', methods=['POST'])
def create_budget():
    """Create a new budget"""
    try:
        category = request.json['category']
        asigned = request.json['asigned']
        activity = request.json['activity']
        user_id = request.json['author']
        
        available = asigned - activity

        user = db.session.query(User).filter(User.id == user_id).first()
        budget = Budget(category=category, asigned=asigned, activity=activity, available=available, author=user)

        db.session.add(budget)
        db.session.commit()

        return jsonify({"message": "Budget created succesfully"})
    except Exception as e:
        print(f"error creating budget: {e}")
        db.session.rollback()
        return jsonify({"error": f"Error creating budget: {str(e)}"}), 500
    
@app.route('/budget', methods=['GET'])
def get_budget():
    """Get all budget"""
    try:
        budgets = Budget.query.all()
        budgets_list = [format_budget(budget) for budget in budgets]
        return jsonify({"budgets": budgets_list})
    except Exception as e:
        print(f"Error retrieving budgets: {e}")
        return jsonify({"error": f"Error retrieving budgets: {str(e)}"})


@app.route('/budget/<int:budget_id>', methods=['GET'])
def get_budget_by_id(budget_id):
    """Get a specific budget by ID"""
    try:
        budget = Budget.query.get(budget_id)

        if not budget:
            return jsonify({"error": "Budget not found"}), 404

        return jsonify({"budget": format_budget(budget)})
    except Exception as e:
        print(f"Error retrieving budget: {e}")
        return jsonify({"error": f"Error retrieving budget: {str(e)}"}), 500



@app.route('/budget/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    """Update a budget"""
    try:
        budget = Budget.query.get(budget_id)

        if not budget:
            return jsonify({"error": "Budget not found"}), 404

        category = request.json.get("category", budget.category)
        asigned = request.json.get("asigned", budget.asigned)
        activity = request.json.get("activity", budget.activity)
        available = asigned - activity

        budget.category = category
        budget.asigned = asigned
        budget.activity = activity
        budget.available = available

        db.session.commit()

        return jsonify({"message": "Budget updated successfully"})
    except Exception as e:
        print(f"Error updating budget: {e}")
        db.session.rollback()
        return jsonify({"error": f"Error updating budget: {str(e)}"}), 500


@app.route('/budget/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    try:
        budget = Budget.query.get(budget_id)

        if not budget:
            return jsonify({"error": "Budget not found"}), 404

        db.session.delete(budget)
        db.session.commit()

        return jsonify({"message": "Budget deleted successfully"})
    except Exception as e:
        print(f"Error deleting budget: {e}")
        db.session.rollback()
        return jsonify({"error": f"Error deleting budget: {str(e)}"}), 500