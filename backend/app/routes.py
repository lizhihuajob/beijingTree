from flask import Blueprint, jsonify, request
from app import db
from app.models import Plant, VisitLog

api_bp = Blueprint('api', __name__)

@api_bp.before_request
def log_visit():
    try:
        visit = VisitLog(
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            path=request.path,
            method=request.method
        )
        db.session.add(visit)
        db.session.commit()
    except:
        pass

@api_bp.route('/plants', methods=['GET'])
def get_plants():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    search = request.args.get('search', '', type=str)
    family = request.args.get('family', '', type=str)
    zone = request.args.get('zone', '', type=str)
    
    query = Plant.query
    
    if search:
        search = f'%{search}%'
        query = query.filter(
            (Plant.name_cn.ilike(search)) |
            (Plant.name_latin.ilike(search)) |
            (Plant.family.ilike(search)) |
            (Plant.genus.ilike(search)) |
            (Plant.description.ilike(search))
        )
    
    if family:
        query = query.filter(Plant.family == family)
    
    if zone:
        query = query.filter(Plant.garden_zones.contains([zone]))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'plants': [plant.to_dict() for plant in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    })

@api_bp.route('/plants/<plant_id>', methods=['GET'])
def get_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    return jsonify(plant.to_dict())

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    total = Plant.query.count()
    
    families = db.session.query(Plant.family).distinct().all()
    families = [f[0] for f in families if f[0]]
    
    protected = Plant.query.filter(Plant.protection_status.isnot(None)).filter(Plant.protection_status != '').count()
    
    zones = set()
    all_plants = Plant.query.all()
    for plant in all_plants:
        if plant.garden_zones:
            zones.update(plant.garden_zones)
    
    return jsonify({
        'total': total,
        'families': len(families),
        'protected': protected,
        'zones': len(zones)
    })

@api_bp.route('/families', methods=['GET'])
def get_families():
    families = db.session.query(Plant.family).distinct().all()
    families = sorted([f[0] for f in families if f[0]])
    return jsonify({'families': families})

@api_bp.route('/zones', methods=['GET'])
def get_zones():
    zones = set()
    all_plants = Plant.query.all()
    for plant in all_plants:
        if plant.garden_zones:
            zones.update(plant.garden_zones)
    return jsonify({'zones': sorted(list(zones))})

@api_bp.route('/protected', methods=['GET'])
def get_protected_plants():
    plants = Plant.query.filter(Plant.protection_status.isnot(None)).filter(Plant.protection_status != '').all()
    return jsonify({'plants': [plant.to_dict() for plant in plants]})

@api_bp.route('/plants/<plant_id>', methods=['PUT'])
def update_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(plant, key):
            setattr(plant, key, value)
    
    db.session.commit()
    return jsonify(plant.to_dict())

@api_bp.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    
    if not data.get('id') or not data.get('name_cn'):
        return jsonify({'error': 'id and name_cn are required'}), 400
    
    if Plant.query.get(data['id']):
        return jsonify({'error': 'Plant with this id already exists'}), 400
    
    plant = Plant(**data)
    db.session.add(plant)
    db.session.commit()
    
    return jsonify(plant.to_dict()), 201

@api_bp.route('/plants/<plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    
    db.session.delete(plant)
    db.session.commit()
    return jsonify({'message': 'Plant deleted successfully'})

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'})
