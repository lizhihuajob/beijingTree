import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin_app import create_admin_app, db
from app.models import Admin

def init_admin():
    app = create_admin_app()
    
    with app.app_context():
        db.create_all()
        
        existing_admin = Admin.query.filter_by(username='admin').first()
        
        if existing_admin:
            print("管理员账号已存在")
            return
        
        admin = Admin(username='admin', email='admin@example.com')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        
        print("管理员账号创建成功!")
        print("用户名: admin")
        print("密码: admin")

if __name__ == '__main__':
    init_admin()
