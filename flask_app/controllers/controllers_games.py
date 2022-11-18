from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_game import Game
from flask_app.models.models_user import User
from flask import flash

# Dashboard
@app.route('/dashboard')
def information():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_by_id(user_data)
    all = Game.get_all_players()
    return render_template('dashboard.html', user = user, all = all)

# Host A Game
@app.route('/add')
def add():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('newpost.html')

@app.route('/create', methods=['POST'])
def create():
    data = {
        'title' : request.form['title'],
        'system' : request.form['system'],
        'location' : request.form['location'],
        'date' : request.form['date'],
        'max_players' : request.form['max_players'],
        'description' : request.form['description'],
        'user_id' : session['user_id']
    }
    if not Game.game_validator(data):
        return redirect('/add')
    Game.create(data)
    return redirect('/dashboard')

# Edit Game
@app.route('/edit/<int:game_id>')
def edit(game_id):
    data = {
        'id' : game_id
    }
    game = Game.get_one(data)
    return render_template('editpost.html', game = game)

@app.route('/update/<int:game_id>', methods=['POST'])
def update(game_id):
    data = {
        'id' : game_id,
        'title' : request.form['title'],
        'system' : request.form['system'],
        'location' : request.form['location'],
        'date' : request.form['date'],
        'max_players' : request.form['max_players'],
        'description' : request.form['description']
    }
    if not Game.game_validator(data):
        return redirect(f'/edit/{game_id}')
    Game.update(data)
    return redirect('/dashboard')

# Show Game
@app.route('/show/<int:game_id>')
def show(game_id):
    data = {
        'id' : game_id
    }
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_by_id(user_data)
    game = Game.get_one(data)
    all = Game.get_all_players()
    return render_template('game.html', user = user, game = game, all = all)

# Delete Game
@app.route('/delete/<int:game_id>')
def delete(game_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : game_id
    }
    Game.delete(data)
    return redirect('/dashboard')

# Join/Leave Game
@app.route('/join/<int:game_id>')
def join(game_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'game_id' : game_id,
        'user_id' : session['user_id']
    }
    Game.join(data)
    return redirect('/dashboard')

@app.route('/leave/<int:game_id>')
def leave(game_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'game_id' : game_id,
        'user_id' : session['user_id']
    }
    Game.leave(data)
    return redirect('/dashboard')