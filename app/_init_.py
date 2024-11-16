from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_sharing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'your_password'  # Replace with your email password

    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.routes import api_blueprint
        app.register_blueprint(api_blueprint)

        db.create_all()

    return app
