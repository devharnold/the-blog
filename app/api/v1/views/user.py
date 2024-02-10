#!/usr/bin/python3
"""handling all default Restful API actions for user"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/user', methods=['GET'])
def get_user():
    """Retrieves the list of the User objects"""
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)

@app_views.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves list of users based on their IDs"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/user', methods=['POST'])
def post_user():
    """Creates a user object"""
    if not request.get_json():
        abort(404, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(404, description="Missing email")
    if 'password' not in request.get_json():
        abort(404, description="Missing password")
    
    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/user/<user_id>', methods=['PUT'])
def put_user(user_id):
    """Updates a user's object in relation to the user id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a json")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)