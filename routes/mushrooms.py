# routes/mushrooms.py
from flask import Blueprint, jsonify, request
from flask_restx import Resource, Api, fields, Namespace
from models import db, Mushroom
from .validation_helpers import validate_mushroom_data

mushrooms_bp = Blueprint('mushrooms', __name__)
api = Api(mushrooms_bp, version='1.0', title='Mushrooms API', description='CRUD operations for mushrooms')

namespace = Namespace('mushrooms', description='Mushroom operations')
api.add_namespace(namespace)

# Define a data model for the Mushroom resource
mushroom_model = api.model('Mushroom', {
    'id': fields.Integer(readonly=True, description='The mushroom identifier'),
    'name': fields.String(required=True, description='The mushroom name'),
    'description': fields.String(description='The mushroom description'),
    'edible': fields.Boolean(description='Is the mushroom edible?')
})

@namespace.route('/mushrooms')
class MushroomsResource(Resource):
    @namespace.marshal_with(mushroom_model, envelope='mushrooms')
    def get(self):
        """Get all mushrooms"""
        try:
            mushrooms = Mushroom.query.all()
            return mushrooms
        except Exception as e:
            api.abort(500, 'Internal Server Error', error=str(e))

    @namespace.expect(mushroom_model)
    @namespace.marshal_with(mushroom_model, envelope='mushroom')
    def post(self):
        """Create a new mushroom"""
        try:
            data = request.json
            is_valid, validation_error = validate_mushroom_data(data)
            if not is_valid:
                api.abort(400, 'Validation error', errors=validation_error)

            new_mushroom = Mushroom(name=data['name'], description=data.get('description', ''), edible=data.get('edible', False))
            db.session.add(new_mushroom)
            db.session.commit()
            return new_mushroom, 201
        except Exception as e:
            db.session.rollback()
            api.abort(500, 'Internal Server Error', error=str(e))

@namespace.route('/mushrooms/<int:mushroom_id>')
@namespace.response(404, 'Mushroom not found')
@namespace.param('mushroom_id', 'The mushroom identifier')
class MushroomResource(Resource):
    @namespace.marshal_with(mushroom_model, envelope='mushroom')
    def get(self, mushroom_id):
        """Get a specific mushroom"""
        try:
            mushroom = Mushroom.query.get_or_404(mushroom_id)
            return mushroom
        except Exception as e:
            api.abort(500, 'Internal Server Error', error=str(e))

    @namespace.expect(mushroom_model)
    @namespace.marshal_with(mushroom_model, envelope='mushroom')
    def put(self, mushroom_id):
        """Update a mushroom"""
        try:
            mushroom = Mushroom.query.get_or_404(mushroom_id)
            data = request.json
            is_valid, validation_error = validate_mushroom_data(data)
            if not is_valid:
                api.abort(400, 'Validation error', errors=validation_error)

            mushroom.name = data.get('name', mushroom.name)
            mushroom.description = data.get('description', mushroom.description)
            mushroom.edible = data.get('edible', mushroom.edible)
            db.session.commit()
            return mushroom
        except Exception as e:
            db.session.rollback()
            api.abort(500, 'Internal Server Error', error=str(e))

    @namespace.response(204, 'Mushroom deleted')
    def delete(self, mushroom_id):
        """Delete a mushroom"""
        try:
            mushroom = Mushroom.query.get_or_404(mushroom_id)
            db.session.delete(mushroom)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            api.abort(500, 'Internal Server Error', error=str(e))
