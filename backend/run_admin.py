import os
from admin_app import create_admin_app

app = create_admin_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
