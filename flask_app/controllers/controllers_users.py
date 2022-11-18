from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_user import User
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

# Register
@app.route('/register', methods=['POST'])
def register():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'username' : request.form['username'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password']
    }
    if not User.user_validator(data):
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(data['password'])
    session['user_id'] = User.register(data)
    return redirect('/dashboard')

# Login
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }
    if not User.login_validator(data):
        return redirect('/')
    user_exists = User.get_by_email(data)
    if not user_exists:
        flash('Invalid email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_exists.password, data['password']):
        flash('Invalid email or password', 'login')
        return redirect('/')
    session['user_id'] = user_exists.id
    return redirect('/dashboard')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')