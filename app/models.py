# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mushroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    edible = db.Column(db.Boolean, default=False)
