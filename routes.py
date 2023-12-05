# routes.py
from flask import Blueprint, jsonify, request
from models import db, Mushroom

mushrooms_bp = Blueprint('mushrooms', __name__)

# Get all mushrooms
@mushrooms_bp.route('/mushrooms', methods=['GET'])
def get_mushrooms():
    mushrooms = Mushroom.query.all()
    mushroom_list = [{'id': m.id, 'name': m.name, 'description': m.description, 'edible': m.edible} for m in mushrooms]
    return jsonify({'mushrooms': mushroom_list})

# Get a specific mushroom
@mushrooms_bp.route('/mushrooms/<int:mushroom_id>', methods=['GET'])
def get_mushroom(mushroom_id):
    mushroom = Mushroom.query.get_or_404(mushroom_id)
    return jsonify({'mushroom': {'id': mushroom.id, 'name': mushroom.name, 'description': mushroom.description, 'edible': mushroom.edible}})

# Create a new mushroom
@mushrooms_bp.route('/mushrooms', methods=['POST'])
def create_mushroom():
    data = request.json
    new_mushroom = Mushroom(name=data['name'], description=data.get('description', ''), edible=data.get('edible', False))
    db.session.add(new_mushroom)
    db.session.commit()
    return jsonify({'mushroom': {'id': new_mushroom.id, 'name': new_mushroom.name, 'description': new_mushroom.description, 'edible': new_mushroom.edible}}), 201

# Update a mushroom
@mushrooms_bp.route('/mushrooms/<int:mushroom_id>', methods=['PUT'])
def update_mushroom(mushroom_id):
    mushroom = Mushroom.query.get_or_404(mushroom_id)
    data = request.json
    mushroom.name = data.get('name', mushroom.name)
    mushroom.description = data.get('description', mushroom.description)
    mushroom.edible = data.get('edible', mushroom.edible)
    db.session.commit()
    return jsonify({'mushroom': {'id': mushroom.id, 'name': mushroom.name, 'description': mushroom.description, 'edible': mushroom.edible}})

# Delete a mushroom
@mushrooms_bp.route('/mushrooms/<int:mushroom_id>', methods=['DELETE'])
def delete_mushroom(mushroom_id):
    mushroom = Mushroom.query.get_or_404(mushroom_id)
    db.session.delete(mushroom)
    db.session.commit()
    return jsonify({'message': 'Mushroom deleted'})
