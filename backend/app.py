from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, 
        static_folder='../frontend',
        static_url_path=''
    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 3306)}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    
    # JWT + CORS
    JWTManager(app)
    CORS(app, origins=[os.getenv('FRONTEND_URL', 'http://localhost:5000')])

    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.hr import hr_bp
    from routes.employee import employee_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(hr_bp, url_prefix='/api/hr')
    app.register_blueprint(employee_bp, url_prefix='/api/employee')

    # Serve frontend
    @app.route('/')
    def index():
        return send_from_directory('../frontend', 'index.html')
    
    @app.route('/<path:path>')
    def static_files(path):
        return send_from_directory('../frontend', path)

    return app
