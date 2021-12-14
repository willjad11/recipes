from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

class User:

    def __init__(self, data):

        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at ) VALUES ( %(fname)s , %(lname)s , %(em)s , %(pas)s , NOW() , NOW() );"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(em)s;"
        result = connectToMySQL("recipes").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("recipes").query_db(query, data)
        # Didn't find a matching user
        if not result:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['em']):
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_pass(pas):
        is_valid = True
        if not PASS_REGEX.match(pas):
            is_valid = False
        return is_valid
    
    @staticmethod
    def is_duplicate(data):
        is_dup = False
        query = "SELECT * FROM email where email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        if results:
            if results[0]['email'] == data['email']:
                is_dup = True
        return is_dup

    @staticmethod
    def validate_registration(form):
        valid = True
        if len(form['fname']) < 2:
            flash("First name must be at least 2 characters in length.", 'register1')
            valid = False
        if len(form['lname']) < 2:
            flash("Last name must be at least 2 characters in length.", 'register2')
            valid = False
        if not User.validate_email(form):
            flash("Invalid email address!", 'register3')
            valid = False
        if User.is_duplicate({"em": form['em']}):
            flash("Email is already registered with another account.", 'register3')
            valid = False
        if not User.validate_pass(form['pas']):
            flash("Password must be minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!", 'register4')
            valid = False
        if form['pas'] != form['cpas']:
            flash("Passwords do not match!", 'register4')
            valid = False
        return valid

    @staticmethod
    def validate_login(form):
        valid = True
        user_in_db = User.get_by_email({"em": form["em"]})
        if not user_in_db:
            flash("Invalid Email/Password", 'login')
            valid = False
            return valid
        if not bcrypt.check_password_hash(user_in_db.password, form['pas']):
            flash("Invalid Email/Password", 'login')
            valid = False
            return valid
        if valid == True:
            session['user_id'] = user_in_db.id
            session['first_name'] = user_in_db.first_name
            session['last_name'] = user_in_db.last_name
        return valid
