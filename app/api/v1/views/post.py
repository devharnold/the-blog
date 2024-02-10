#!/usr/bin/python3
"""handles all default Restful API actions for posts"""
from models.posts import Posts
from models import storage
from api.v1.views import app_views
from flask import request, make_response, jsonify, abort

@app_views.route('/posts', method=['GET'])
def get_posts():
    """retrieves lists of all posts"""
    all_posts = storage.all(Posts).values()
    list_posts = []
    for post in all_posts:
        list_posts.append(post.to_dict)
    return jsonify(list_posts)

@app_views.route('/posts/<post_id>', method=['GET'])
def get_post(post_id):
    """Retrieves posts according to their respective IDs"""
    post = storage.get(Posts, post_id)
    if not post:
        abort(404)
    return jsonify(post.to_dict())

@app_views.route('/post/<post_id>', method=['DELETE'])
def delete_post(post_id):
    """Deletes a post based on it's ID"""
    post = storage.get(Posts, post_id)
    if not post:
        abort(404)
    storage.delete(post)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/post', method=['POST'])
def create_post():
    """Creates a post"""
    if not request.get_json():
        abort(400, description="Not a json")

    if 'title' not in request.get_json():
        abort(400, description="Missing post title")
    
    data = request.get_json()
    instance = Posts(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/post/<post_id>', method=['PUT'])
def update_post(post_id):
    """Updates a user's post based on the specific ID"""
    post = storage.get(Posts, post_id)
    if not post:
        abort(404)
    if not request.get_json():
        abort(404, description="Not a JSON")

    ignore = ['id', 'title', 'name', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(post, key, value)
    storage.save()
    return make_response(jsonify(post.to_dict()), 200)
