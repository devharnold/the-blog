#!/usr/bin/python3
"""handles all default Restful API actions for settings"""
from models.settings import Settings
from models import storage
from api.v1.views import app_views
from flask import request, make_response, jsonify, abort

@app_views.route('/settings', method=['GET'])
def get_posts():
    """retrieves lists of all posts"""
    all_settings = storage.all(Settings).values()
    list_settings = []
    for setting in all_settings:
        list_settings.append(setting.to_dict)
    return jsonify(list_settings)

@app_views.route('/settings/<setting_id>', method=['GET'])
def get_post(setting_id):
    """Retrieves settings according to their respective IDs"""
    setting = storage.get(Settings, setting_id)
    if not setting:
        abort(404)
    return jsonify(setting.to_dict())

@app_views.route('/setting/<setting_id>', method=['DELETE'])
def delete_post(setting_id):
    """Deletes a post based on it's ID"""
    setting = storage.get(Settings, setting_id)
    if not setting:
        abort(404)
    storage.delete(setting)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/setting', method=['POST'])
def post_setting():
    """Creates a post"""
    if not request.get_json():
        abort(400, description="Not a json")

    if 'name' not in request.get_json():
        abort(400, description="Missing setting name")
    
    data = request.get_json()
    instance = Settings(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/settings/<setting_id>', method=['PUT'])
def update_setting(setting_id):
    """Updates a user's post based on the specific ID"""
    setting = storage.get(Settings, setting_id)
    if not setting:
        abort(404)
    if not request.get_json():
        abort(404, description="Not a JSON")

    ignore = ['id', 'title', 'name', 'created_at', 'updated_at', 'password', 'email']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(setting, key, value)
    storage.save()
    return make_response(jsonify(setting.to_dict()), 200)