#!/usr/bin/python3
"""Blueprint for API v1 views"""
from flask import Blueprint, app

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.post import *
from api.v1.views.settings import *
from api.v1.views.user import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)