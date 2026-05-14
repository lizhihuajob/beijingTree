import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Plant

def find_data_file():
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'plants_with_real_images.json'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'plants.json'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frontend', 'src', 'data', 'plants.json'),
        '/app/data/plants_with_real_images.json',
        '/app/data/plants.json',
        '/app/frontend_data/plants.json',
        'plants.json'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"找到数据文件: {path}")
            return path
    
    print("未找到任何数据文件，尝试列出当前目录:")
    try:
        print(os.listdir('.'))
        if os.path.exists('/app'):
            print("/app 目录内容:", os.listdir('/app'))
        if os.path.exists('/app/data'):
            print("/app/data 目录内容:", os.listdir('/app/data'))
        if os.path.exists('/app/frontend_data'):
            print("/app/frontend_data 目录内容:", os.listdir('/app/frontend_data'))
    except:
        pass
    return None

def init_database():
    print("开始初始化数据库...")
    app = create_app()
    print(f"数据库URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    max_retries = 5
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
                print("数据库表创建完成")
                
                if Plant.query.first() is not None:
                    print("数据库已存在数据，跳过初始化")
                    return
                
                json_path = find_data_file()
                if not json_path:
                    print("错误: 找不到任何数据文件")
                    return
                
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    plants_data = data.get('plants', [])
                    print(f"读取到 {len(plants_data)} 条植物数据")
                    
                    if len(plants_data) == 0:
                        print("警告: JSON 文件中没有植物数据")
                        return
                    
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
                    return
                except Exception as e:
                    print(f"初始化数据库时发生错误: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    db.session.rollback()
                    raise
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"数据库连接失败，{retry_delay}秒后重试... (尝试 {attempt + 1}/{max_retries})")
                import time
                time.sleep(retry_delay)
            else:
                print(f"数据库初始化失败，已重试 {max_retries} 次")
                raise

if __name__ == '__main__':
    init_database()
