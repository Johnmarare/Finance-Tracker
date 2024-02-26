from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa

from app import app, db
from app.models import User

@app.route("/api/signup", methods=["POST"])
def signup():
    """creates a user"""
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created succesfully"})


@app.route("/api/login", methods=["POST"])
def login():
    """login for user"""
    data = request.json
    username = data.get("username")
    pasword = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, pasword):
        return jsonify({"message": "Login succesful"})
    else:
        return jsonify({"message": "Invalid credentials! check username or password."}), 401
    
