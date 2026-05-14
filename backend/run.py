import os
import atexit
from app import create_app
from app.scheduler import start_scheduler

app = create_app(os.getenv('FLASK_ENV', 'default'))

scheduler = None

if os.getenv('ENABLE_SCHEDULER', 'true').lower() == 'true':
    scheduler = start_scheduler()
    atexit.register(lambda: scheduler.shutdown() if scheduler else None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
