from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config.config import config

db = SQLAlchemy()

def create_admin_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    CORS(app, resources={r"/admin/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    db.init_app(app)
    
    from admin_app.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin/api')
    
    return app
