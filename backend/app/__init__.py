from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import models, expense_routes, income_routes, budget_routes, auth_routes
