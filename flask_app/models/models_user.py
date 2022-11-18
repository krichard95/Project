from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

db = "game_site"

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.games = []

# Register New
    @classmethod
    def register(cls, data):
        query = """ 
                INSERT INTO users (first_name, last_name, email, username, password)
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password)s )
                """
        return connectToMySQL(db).query_db(query, data)

# Login
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

# Validate
    @staticmethod
    def user_validator(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid= True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        email_results = connectToMySQL(db).query_db(query, data)
        if len(email_results) > 0:
            flash('Email already registered', 'register')
            is_valid = False
            return is_valid
        query = "SELECT * FROM users WHERE username = %(username)s;"
        username_results = connectToMySQL(db).query_db(query, data)
        if len(username_results) > 0:
            flash('Username already taken', 'register')
            is_valid = False
            return is_valid
        if len(data['first_name']) == 0:
            flash('All fields are required', 'register')
            is_valid = False
            return is_valid
        if len(data['last_name']) == 0:
            flash('All fields are required', 'register')
            is_valid = False
            return is_valid
        if len(data['email']) == 0:
            flash('All fields are required', 'register')
            is_valid = False
            return is_valid
        if len(data['username']) == 0:
            flash('All fields are required', 'register')
            is_valid = False
            return is_valid
        if len(data['password']) == 0:
            flash('All fields are required', 'register')
            is_valid = False
            return is_valid
        if not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!', 'register')
            is_valid = False
            return is_valid
        if len(data['first_name']) < 3:
            flash('First name must be at least 3 characters.', 'register')
            is_valid = False
        if str.isalpha(data['first_name']) == False:
            flash('First name must contain only letters.', 'register')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name must be at least 3 characters.', 'register')
            is_valid = False
        if str.isalpha(data['last_name']) == False:
            flash('Last name must contain only letters.', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters.', 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match.', 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def login_validator(data):
        is_valid= True
        if len(data['email']) == 0:
            flash('All fields are required', 'login')
            is_valid = False
            return is_valid
        if len(data['password']) == 0:
            flash('All fields are required', 'login')
            is_valid = False
            return is_valid
        return is_valid