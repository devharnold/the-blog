#!/usr/bin/python3
"""Flask app"""

from models import storage
from api.v1.views import app_views
from api.v1 import v1
from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(v1)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage connection when the application context is torn down
    The function is registered to be called automatically when the application
    context is about to be torn down, ensuring that the storage connection is
    properly closed. Helps with resource management and cleanup
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Error: 404
    ------------
    responses: 
    404: description=`a rsource was not found`
    """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'the-blog Restful API',
    'uiversion': 5.11
}
Swagger(app)

if __name__ == "__main__":
    host = environ.get('THEBLOG_API_HOST', '0.0.0.0')
    port = int(environ.get('THEBLOG_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)