from flask import Flask
from extensions import db, login_manager
from config import Config
import os

def init_db(app):
    from models.user import User
    from models.client import Client
    
    with app.app_context():
        db.create_all()
        
        try:
            # Create mock admin if not exists
            if not User.query.filter_by(email='admin@coderon.com').first():
                admin = User(
                    email='admin@coderon.com',
                    is_admin=True
                )
                admin.set_password('admin123')
                db.session.add(admin)

            # Create mock clients
            clients_data = [
                {
                    'name': 'Tech Corp',
                    'email': 'tech@example.com',
                    'password': 'client123'
                },
                {
                    'name': 'Design Studio',
                    'email': 'design@example.com',
                    'password': 'client123'
                }
            ]

            for client_data in clients_data:
                if not Client.query.filter_by(email=client_data['email']).first():
                    client = Client(
                        name=client_data['name'],
                        email=client_data['email']
                    )
                    client.set_password(client_data['password'])
                    db.session.add(client)

            db.session.commit()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")
            db.session.rollback()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure instance folder exists
    os.makedirs('instance', exist_ok=True)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.client import client_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)

    # Initialize database
    init_db(app)

    return app

if __name__ == '__main__':
    # Delete the existing database file if it exists
    if os.path.exists('instance/database.db'):
        os.remove('instance/database.db')
        print("Removed existing database file")

    app = create_app()
    app.run(debug=True)