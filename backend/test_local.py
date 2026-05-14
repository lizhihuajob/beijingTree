#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from app.models import Plant

def test_database():
    print("=== 测试数据库初始化 ===")
    app = create_app('development')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test_plants.db'
    
    with app.app_context():
        db.create_all()
        print("✓ 数据库表创建成功")
        
        count = Plant.query.count()
        print(f"✓ 当前数据库中有 {count} 条记录")
        
        if count == 0:
            print("数据库为空，开始导入数据...")
            from scripts.init_db import find_data_file
            import json
            
            json_path = find_data_file()
            if json_path:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                plants_data = data.get('plants', [])
                for plant_data in plants_data[:5]:
                    plant = Plant(**{k: v for k, v in plant_data.items() if k in Plant.__table__.columns.keys()})
                    db.session.add(plant)
                db.session.commit()
                print(f"✓ 成功导入 {len(plants_data[:5])} 条测试数据")
            else:
                print("✗ 找不到数据文件")
                return False
        
        plants = Plant.query.limit(3).all()
        for plant in plants:
            print(f"  - {plant.name_cn} ({plant.family})")
    
    return True

def test_api():
    print("\n=== 测试 API 端点 ===")
    app = create_app('development')
    
    with app.test_client() as client:
        response = client.get('/api/health')
        print(f"健康检查: {response.status_code} - {response.json}")
        
        response = client.get('/api/plants?per_page=5')
        print(f"获取植物列表: {response.status_code}")
        if response.status_code == 200:
            data = response.json
            print(f"  总数: {data.get('total')}, 当前页: {len(data.get('plants', []))}")
        
        response = client.get('/api/statistics')
        print(f"统计信息: {response.status_code} - {response.json}")
        
        response = client.get('/api/families')
        print(f"科属列表: {response.status_code} - {len(response.json.get('families', []))} 个")
        
    return True

if __name__ == '__main__':
    try:
        test_database()
        test_api()
        print("\n=== 所有测试完成 ===")
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
