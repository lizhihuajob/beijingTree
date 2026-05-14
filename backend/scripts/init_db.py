import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Plant

def init_database():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        if Plant.query.first() is not None:
            print("数据库已存在数据，跳过初始化")
            return
        
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'plants_with_real_images.json')
        
        if not os.path.exists(json_path):
            print(f"找不到数据文件: {json_path}")
            json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frontend', 'src', 'data', 'plants.json')
            if not os.path.exists(json_path):
                print(f"也找不到数据文件: {json_path}")
                return
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        plants_data = data.get('plants', [])
        
        for plant_data in plants_data:
            plant = Plant(
                id=plant_data.get('id'),
                name_cn=plant_data.get('name_cn'),
                name_latin=plant_data.get('name_latin'),
                family=plant_data.get('family'),
                genus=plant_data.get('genus'),
                common_names=plant_data.get('common_names'),
                description=plant_data.get('description'),
                detailed_description=plant_data.get('detailed_description'),
                morphology=plant_data.get('morphology'),
                habitat=plant_data.get('habitat'),
                distribution=plant_data.get('distribution'),
                garden_zones=plant_data.get('garden_zones'),
                protection_status=plant_data.get('protection_status'),
                iucn_status=plant_data.get('iucn_status'),
                uses=plant_data.get('uses'),
                medicinal_uses=plant_data.get('medicinal_uses'),
                ornamental_value=plant_data.get('ornamental_value'),
                ecological_value=plant_data.get('ecological_value'),
                cultural_significance=plant_data.get('cultural_significance'),
                flowering_period=plant_data.get('flowering_period'),
                fruiting_period=plant_data.get('fruiting_period'),
                light_requirements=plant_data.get('light_requirements'),
                water_requirements=plant_data.get('water_requirements'),
                soil_preference=plant_data.get('soil_preference'),
                temperature_range=plant_data.get('temperature_range'),
                hardiness_zone=plant_data.get('hardiness_zone'),
                growth_rate=plant_data.get('growth_rate'),
                lifespan=plant_data.get('lifespan'),
                max_height=plant_data.get('max_height'),
                max_width=plant_data.get('max_width'),
                leaf_type=plant_data.get('leaf_type'),
                flower_color=plant_data.get('flower_color'),
                fruit_color=plant_data.get('fruit_color'),
                image_urls=plant_data.get('image_urls'),
                primary_image=plant_data.get('primary_image'),
                source_url=plant_data.get('source_url'),
                collected_at=plant_data.get('collected_at'),
                notes=plant_data.get('notes'),
                image_source=plant_data.get('image_source')
            )
            db.session.add(plant)
        
        db.session.commit()
        print(f"成功初始化数据库，导入 {len(plants_data)} 条植物数据")

if __name__ == '__main__':
    init_database()
