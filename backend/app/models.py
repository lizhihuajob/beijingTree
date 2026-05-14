from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SpiderConfig(db.Model):
    __tablename__ = 'spider_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    frequency_type = db.Column(db.String(20), default='daily')
    cron_hour = db.Column(db.Integer, default=2)
    cron_minute = db.Column(db.Integer, default=0)
    interval_minutes = db.Column(db.Integer, default=60)
    last_run_at = db.Column(db.DateTime)
    next_run_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'enabled': self.enabled,
            'frequency_type': self.frequency_type,
            'cron_hour': self.cron_hour,
            'cron_minute': self.cron_minute,
            'interval_minutes': self.interval_minutes,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'next_run_at': self.next_run_at.isoformat() if self.next_run_at else None
        }

class VisitLog(db.Model):
    __tablename__ = 'visit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    path = db.Column(db.String(200))
    method = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'path': self.path,
            'method': self.method,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class Plant(db.Model):
    __tablename__ = 'plants'
    
    id = db.Column(db.String(100), primary_key=True)
    name_cn = db.Column(db.String(200), nullable=False, index=True)
    name_latin = db.Column(db.String(200))
    family = db.Column(db.String(100), index=True)
    genus = db.Column(db.String(100))
    common_names = db.Column(db.JSON)
    description = db.Column(db.Text)
    detailed_description = db.Column(db.Text)
    morphology = db.Column(db.Text)
    habitat = db.Column(db.Text)
    distribution = db.Column(db.Text)
    garden_zones = db.Column(db.JSON)
    protection_status = db.Column(db.String(100))
    iucn_status = db.Column(db.String(100))
    uses = db.Column(db.JSON)
    medicinal_uses = db.Column(db.Text)
    ornamental_value = db.Column(db.Text)
    ecological_value = db.Column(db.Text)
    cultural_significance = db.Column(db.Text)
    flowering_period = db.Column(db.String(100))
    fruiting_period = db.Column(db.String(100))
    light_requirements = db.Column(db.String(200))
    water_requirements = db.Column(db.String(200))
    soil_preference = db.Column(db.String(200))
    temperature_range = db.Column(db.String(200))
    hardiness_zone = db.Column(db.String(100))
    growth_rate = db.Column(db.String(100))
    lifespan = db.Column(db.String(100))
    max_height = db.Column(db.String(100))
    max_width = db.Column(db.String(100))
    leaf_type = db.Column(db.String(200))
    flower_color = db.Column(db.String(200))
    fruit_color = db.Column(db.String(200))
    image_urls = db.Column(db.JSON)
    primary_image = db.Column(db.String(500))
    source_url = db.Column(db.String(500))
    collected_at = db.Column(db.String(100))
    notes = db.Column(db.Text)
    image_source = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name_cn': self.name_cn,
            'name_latin': self.name_latin,
            'family': self.family,
            'genus': self.genus,
            'common_names': self.common_names or [],
            'description': self.description,
            'detailed_description': self.detailed_description,
            'morphology': self.morphology,
            'habitat': self.habitat,
            'distribution': self.distribution,
            'garden_zones': self.garden_zones or [],
            'protection_status': self.protection_status,
            'iucn_status': self.iucn_status,
            'uses': self.uses or [],
            'medicinal_uses': self.medicinal_uses,
            'ornamental_value': self.ornamental_value,
            'ecological_value': self.ecological_value,
            'cultural_significance': self.cultural_significance,
            'flowering_period': self.flowering_period,
            'fruiting_period': self.fruiting_period,
            'light_requirements': self.light_requirements,
            'water_requirements': self.water_requirements,
            'soil_preference': self.soil_preference,
            'temperature_range': self.temperature_range,
            'hardiness_zone': self.hardiness_zone,
            'growth_rate': self.growth_rate,
            'lifespan': self.lifespan,
            'max_height': self.max_height,
            'max_width': self.max_width,
            'leaf_type': self.leaf_type,
            'flower_color': self.flower_color,
            'fruit_color': self.fruit_color,
            'image_urls': self.image_urls or [],
            'primary_image': self.primary_image,
            'source_url': self.source_url,
            'collected_at': self.collected_at,
            'notes': self.notes,
            'image_source': self.image_source
        }
