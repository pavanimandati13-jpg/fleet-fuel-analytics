import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from database import db
from routes import api_bp

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')


def create_app():
    app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///fleet.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app, origins=os.getenv('CORS_ORIGIN', '*'))

    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
    db.create_all()

    from seed_data import populate_if_empty
    populate_if_empty()

    @app.route('/')
    def index():
        return send_from_directory(FRONTEND_DIR, 'index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
