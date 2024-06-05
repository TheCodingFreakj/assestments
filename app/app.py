
from flask import Flask
from config import Config
from main.model.models import db  # Import db from models
from flask_migrate import Migrate
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Initialize SQLAlchemy
    db.init_app(app)
    Migrate(app, db)
    # Register blueprints
    from main.service.view import employees_bp
    app.register_blueprint(employees_bp)
    if __name__ == '__main__':
       app.run(debug=True)
    return app   

#import the models
from main.model.models import *
create_app()