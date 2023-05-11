from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os #read environment vairables
from dotenv import load_dotenv #import libraries for grabbing environment variables

#we use access to database operations
db = SQLAlchemy()
migrate = Migrate()
load_dotenv() #load the values from the .enc so the os module is able to see them

def create_app(test_config = None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #due to both environment are false
    #set up database to work on testing or development
    if not test_config:
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")  
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("RENDER_DATABASE_URI")
    else:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI") 

    #connect the db and migrate to our flask app
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import crystal_bp, healer_bp
    app.register_blueprint(crystal_bp)
    app.register_blueprint(healer_bp)

    #import the model
    from app.models.crystal import Crystal    
    from app.models.healer import Healer

    return app