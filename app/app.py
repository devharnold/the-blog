#!usr/bin/python3
from models.base_model import BaseModel, Base
from flask import Flask, render_template
from api.v1.views import app_views


app = Flask(__name__)


@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)