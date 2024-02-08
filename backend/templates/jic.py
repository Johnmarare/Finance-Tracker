#!/usr/bin/python3


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    
    def __repr__(self):
        return f"Expense('{self.description}', '{self.amount}', '{self.date}')"

    def __init__(self, description, amount, date=None):
        self.description = description
        self.amount = amount
        self.date = date if date else datetime.utcnow()


def format_expense(expense):
    return {
        "description": expense.description,
        "amount": expense.amount,
        "created_at": expense.date,
        "id": expense.id
    }



@app.route("/expense", methods = ['POST'])
def create_expense():
    """Create an expense"""
    description = request.json["description"]
    amount = request.json["amount"]

    expense = Expense(description=description, amount=amount, date=datetime.utcnow())
    db.session.add(expense)
    db.session.commit()
    return format_expense(expense)

@app.route("/expense", methods=['GET'])
def get_expense():
    """get expenses"""
    expenses = Expense.query.all()
    expense_list = []
    for expense in expenses:
        expense_list.append(format_expense(expense))
    return {"expenses": expense_list}

@app.route("/expense/<id>", methods=["GET"])
def get_exp(id):
    """retrieve uniquely"""
    expense = Expense.query.filter_by(id=id).one()
    formatted_expense = format_expense(expense)
    return {"expense": formatted_expense}

@app.route("/expense/<id>", methods=["DELETE"])
def delete_expense(id):
    """delete expenses"""
    expense = Expense.query.filter_by(id=id).one()
    db.session.delete(expense)
    db.session.commit()
    return f"Expense (id: {id}) deleted!"

@app.route("/expense/<id>", methods=["PUT"])
def update_expense(id):
    """Updates expenditure"""
    expense = Expense.query.filter_by(id=id)
    description = request.json["description"]
    amount = request.json["amount"]
    expense.update(dict(description=description, amount=amount, created_at=datetime.utcnow()))
    db.session.commit()

    return {"expense": format_expense(expense.one())}


if __name__ == "__main__":
    db.create_all()
    app.run()
