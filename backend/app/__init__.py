from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config.config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    db.init_app(app)
    
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
