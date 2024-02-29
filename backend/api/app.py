from flask import Flask, redirect, url_for, request
from alchemical.flask import Alchemical
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from apifairy import APIFairy
from config import Config

db = Alchemical()
migrate = Migrate()
ma =  Marshmallow()
cors = CORS()
mail = Mail()
apifairy = APIFairy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions
    from api import models
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    # conditional CORS initialization
    if app.config['USE_CORS']:
        cors.init_app(app)
    
    mail.init_app(app)
    apifairy.init_app(app)

    # blueprints
    from api.errors import errors
    app.register_blueprint(errors)
    from api.tokens import tokens
    app.register_blueprint(tokens, url_prefix='/api')
    from api.users import users
    app.register_blueprint(users, url_prefix='/api')
    from api.expense_routes import expenses
    app.register_blueprint(expenses, url_prefix='/api')
    from api.income_routes import incomes
    app.register_blueprint(incomes, url_prefix='/api')
    from api.budget_routes import budgets
    app.register_blueprint(budgets, url_prefix='/api')

    # define shellcontext
    @app.shell_context_processor
    def shell_context():
        ctx = {'db': db}
        for attr in dir(models):
            model = getattr(models, attr)
            if hasattr(model, '__bases__') and \
                    db.Model in getattr(model, '__bases__'):
                ctx[attr] = model
        return ctx
    
    @app.route('/')
    def index():
        return redirect(url_for('apifairy.docs'))
    
    @app.after_request
    def after_request(response):
        # Werkzeug sometimes does not flush the request, thus its done here
        request.get_data()
        return response
    
    return app