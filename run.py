import os
from app import create_app

# os.getenv('APP_SETTINGS')

app = create_app(os.getenv('APP_SETTINGS'))

if __name__ == '__main__':
    app.run()
