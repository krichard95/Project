from flask_app.models.models_user import User
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

db = "game_site"

class Game:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.system = data['system']
        self.location = data['location']
        self.date = data['date']
        self.max_players = data['max_players']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.host = None
        self.all_players = []

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO games (title, `system`, location, date, max_players, description, user_id)
                VALUES (%(title)s, %(system)s, %(location)s, %(date)s, %(max_players)s, %(description)s, %(user_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

# Read Games
    @classmethod
    def get_all_with_host(cls):
        query = """
                SELECT * FROM games
                JOIN users ON games.user_id = users.id
                """
        results = connectToMySQL(db).query_db(query)
        all_games = []
        for row in results:
            game = cls(row)
            games_host_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'username' : row['username'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            game.host = User(games_host_data)
            all_games.append(game)
        return all_games

    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM games 
                JOIN users on users.id = games.user_id
                WHERE games.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        game = cls(results[0])
        user_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'username' : results[0]['username'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
        }
        game.host = User(user_data)
        return game

# Update Game Post
    @classmethod
    def update(cls, data):
        query = """
                UPDATE games
                SET title = %(title)s, `system` = %(system)s, location = %(location)s, date = %(date)s, max_players = %(max_players)s, description = %(description)s
                WHERE id = %(id)s
                """
        return connectToMySQL(db).query_db(query, data)

# Delete Game Post
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM games WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)

# Players Join/Leave
    @classmethod
    def join(cls, data):
        query = """
                INSERT INTO players (user_id, game_id)
                VALUES (%(user_id)s, %(game_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def leave(cls, data):
        query = """
                DELETE FROM players
                WHERE game_id = %(game_id)s
                AND user_id = %(user_id)s
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_players(cls):
        query = """
                SELECT * FROM games
                JOIN users ON users.id = games.user_id
                LEFT JOIN players on games.id = players.game_id
                LEFT JOIN users AS users2 ON users2.id = players.user_id
                """
        results = connectToMySQL(db).query_db(query)
        players = []
        for result in results:
            new_player = True
            player_user_data = {
                'id' : result['users2.id'],
                'first_name' : result['users2.first_name'],
                'last_name' : result['users2.last_name'],
                'email' : result['users2.email'],
                'username' : result['users2.username'],
                'password' : result['users2.password'],
                'created_at' : result['users2.created_at'],
                'updated_at' : result['users2.updated_at']
            }
            if len(players) > 0 and players[len(players) - 1].id == result['id']:
                players[len(players) - 1].all_players.append(User(player_user_data))
                new_player = False
            if new_player:
                join = cls(result)
                user_data = {
                    'id' : result['users.id'],
                    'first_name' : result['first_name'],
                    'last_name' : result['last_name'],
                    'email' : result['email'],
                    'username' : result['username'],
                    'password' : result['password'],
                    'created_at' : result['users.created_at'],
                    'updated_at' : result['users.updated_at']
                }
                user = User(user_data)
                join.user = user
                if result['users2.id'] is not None:
                    join.all_players.append(User(player_user_data))
                players.append(join)
        return players

# Validate
    @staticmethod
    def game_validator(data):
        is_valid= True
        if len(data['title']) == 0:
            flash('All fields are required')
            is_valid = False
            return is_valid
        if len(data['system']) == 0:
            flash('All fields are required')
            is_valid = False
            return is_valid
        if len(data['location']) == 0:
            flash('All fields are required')
            is_valid = False
            return is_valid
        if len(data['date']) == 0:
            flash('All fields are required')
            is_valid = False
            return is_valid
        if len(data['max_players']) == 0:
            flash('All fields are required')
            is_valid = False
            return is_valid
        if len(data['description']) == 0:
            flash('All fields are required')
            is_valid = False
            return is_valid
        if int(data['max_players']) < 1:
            flash('Maximum players must be greater than 0.')
            is_valid = False
        return is_valid