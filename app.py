# app.py
from flask import Flask
from models import db
from routes.mushrooms import mushrooms_bp  # Update import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mushrooms.db'  # Use SQLite database

# Register models and blueprints
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(mushrooms_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
