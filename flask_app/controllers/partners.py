from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import partner
# from flask_app.controllers import
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('index.html')