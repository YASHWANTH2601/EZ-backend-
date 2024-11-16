import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User, File
from app.utils import generate_token, decode_token
from app.email_service import send_verification_email

ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}
api_blueprint = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists!"}), 400

    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = generate_token(email, 'your_secret_key')
    send_verification_email(email, token)

    return jsonify({"message": "User created successfully. Please verify your email."}), 201

@api_blueprint.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    data = decode_token(token, 'your_secret_key')
    if not data:
        return jsonify({"message": "Invalid or expired token!"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        user.is_verified = True
        db.session.commit()
        return jsonify({"message": "Email verified successfully!"}), 200
    return jsonify({"message": "User not found!"}), 404

@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials!"}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({"access_token": access_token}), 200

@api_blueprint.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    user = get_jwt_identity()
    if user['role'] != 'ops':
        return jsonify({"message": "Only Ops User can upload files!"}), 403

    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded!"}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads', filename))

        new_file = File(filename=filename, uploaded_by=user['id'])
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully!"}), 201
    return jsonify({"message": "Invalid file type!"}), 400
