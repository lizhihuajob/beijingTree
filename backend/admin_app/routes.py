from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import jwt
import os
from functools import wraps
from app.models import db, Plant, Admin, SpiderConfig, VisitLog

admin_bp = Blueprint('admin', __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'admin-secret-key-change-in-production')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = Admin.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@admin_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    admin = Admin.query.filter_by(username=username).first()
    if not admin:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not admin.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': admin.id,
        'username': admin.username,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': admin.to_dict()
    })

@admin_bp.route('/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify(current_user.to_dict())

@admin_bp.route('/auth/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({'error': 'Old password and new password are required'}), 400
    
    if not current_user.check_password(old_password):
        return jsonify({'error': 'Old password is incorrect'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
    
    current_user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'})

@admin_bp.route('/plants', methods=['GET'])
@token_required
def get_plants(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Plant.query
    
    if search:
        search = f'%{search}%'
        query = query.filter(
            (Plant.name_cn.ilike(search)) |
            (Plant.name_latin.ilike(search)) |
            (Plant.family.ilike(search))
        )
    
    pagination = query.order_by(Plant.name_cn).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'plants': [plant.to_dict() for plant in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@admin_bp.route('/plants/<plant_id>', methods=['GET'])
@token_required
def get_plant(current_user, plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    return jsonify(plant.to_dict())

@admin_bp.route('/plants', methods=['POST'])
@token_required
def create_plant(current_user):
    data = request.get_json()
    
    if not data.get('id') or not data.get('name_cn'):
        return jsonify({'error': 'id and name_cn are required'}), 400
    
    if Plant.query.get(data['id']):
        return jsonify({'error': 'Plant with this id already exists'}), 400
    
    plant = Plant(**data)
    db.session.add(plant)
    db.session.commit()
    
    return jsonify(plant.to_dict()), 201

@admin_bp.route('/plants/<plant_id>', methods=['PUT'])
@token_required
def update_plant(current_user, plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(plant, key) and key != 'id':
            setattr(plant, key, value)
    
    db.session.commit()
    return jsonify(plant.to_dict())

@admin_bp.route('/plants/<plant_id>', methods=['DELETE'])
@token_required
def delete_plant(current_user, plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    
    db.session.delete(plant)
    db.session.commit()
    return jsonify({'message': 'Plant deleted successfully'})

@admin_bp.route('/dashboard/stats', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    total_plants = Plant.query.count()
    
    families = db.session.query(Plant.family).distinct().all()
    families_count = len([f[0] for f in families if f[0]])
    
    protected_count = Plant.query.filter(
        Plant.protection_status.isnot(None)
    ).filter(Plant.protection_status != '').count()
    
    today = datetime.utcnow().date()
    today_visits = VisitLog.query.filter(
        db.func.date(VisitLog.timestamp) == today
    ).count()
    
    total_visits = VisitLog.query.count()
    
    start_of_week = today - timedelta(days=today.weekday())
    weekly_visits = VisitLog.query.filter(
        VisitLog.timestamp >= start_of_week
    ).count()
    
    zones = set()
    all_plants = Plant.query.all()
    for plant in all_plants:
        if plant.garden_zones:
            zones.update(plant.garden_zones)
    
    return jsonify({
        'total_plants': total_plants,
        'families_count': families_count,
        'protected_count': protected_count,
        'zones_count': len(zones),
        'today_visits': today_visits,
        'total_visits': total_visits,
        'weekly_visits': weekly_visits
    })

@admin_bp.route('/dashboard/visit-trend', methods=['GET'])
@token_required
def get_visit_trend(current_user):
    days = request.args.get('days', 7, type=int)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    trend_data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        next_date = date + timedelta(days=1)
        
        count = VisitLog.query.filter(
            VisitLog.timestamp >= date,
            VisitLog.timestamp < next_date
        ).count()
        
        trend_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    return jsonify({'trend': trend_data})

@admin_bp.route('/spider/config', methods=['GET'])
@token_required
def get_spider_config(current_user):
    config = SpiderConfig.query.first()
    if not config:
        config = SpiderConfig(name='plant-spider')
        db.session.add(config)
        db.session.commit()
    
    return jsonify(config.to_dict())

@admin_bp.route('/spider/config', methods=['PUT'])
@token_required
def update_spider_config(current_user):
    config = SpiderConfig.query.first()
    if not config:
        config = SpiderConfig(name='plant-spider')
        db.session.add(config)
    
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    db.session.commit()
    return jsonify(config.to_dict())

@admin_bp.route('/spider/run-now', methods=['POST'])
@token_required
def run_spider_now(current_user):
    try:
        from app.scheduler import update_plants_data
        update_plants_data()
        return jsonify({'message': 'Spider executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/system/info', methods=['GET'])
@token_required
def get_system_info(current_user):
    import platform
    import sys
    
    db_status = 'connected'
    try:
        db.session.execute('SELECT 1')
    except:
        db_status = 'disconnected'
    
    return jsonify({
        'python_version': platform.python_version(),
        'flask_version': __import__('flask').__version__,
        'database_status': db_status,
        'server_time': datetime.utcnow().isoformat(),
        'system_platform': platform.system(),
        'total_visits': VisitLog.query.count()
    })

@admin_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Admin API is running'})
