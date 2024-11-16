from flask import Flask
from app.models import db
from app.routes import app as routes_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_sharing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
