from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa

from app import app, db
from app.models import User

@app.route("/signup", methods=["POST"])
def signup():
    """creates a user"""
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    hashed_password = generate_password_hash(password, method="sha256")

    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created succesfully"})


@app.route("/login", methods=["POST"])
def login():
    """login for user"""
    data = request.json
    email = data.get("email")
    pasword = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, pasword):
        return jsonify({"message": "Login succesful"})
    else:
        return jsonify({"message": "Invalid email or password"}), 401
    