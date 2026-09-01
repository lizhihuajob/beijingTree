import json
import os
import sys
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app, db
from app.models import Plant

def update_plants_data():
    app = create_app()
    with app.app_context():
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'plants_with_real_images.json')
        
        if not os.path.exists(json_path):
            print(f"[{datetime.now()}] 找不到数据文件: {json_path}")
            return
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            plants_data = data.get('plants', [])
            updated_count = 0
            created_count = 0
            
            for plant_data in plants_data:
                plant = Plant.query.get(plant_data.get('id'))
                if plant:
                    for key, value in plant_data.items():
                        if hasattr(plant, key):
                            setattr(plant, key, value)
                    updated_count += 1
                else:
                    plant = Plant(**plant_data)
                    db.session.add(plant)
                    created_count += 1
            
            db.session.commit()
            print(f"[{datetime.now()}] 数据更新完成: 更新 {updated_count} 条, 新增 {created_count} 条")
        except Exception as e:
            print(f"[{datetime.now()}] 数据更新失败: {str(e)}")
            db.session.rollback()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_plants_data, 'cron', hour=2, minute=0)
    scheduler.start()
    print("定时任务已启动，每天凌晨 2 点更新数据")
    return scheduler
