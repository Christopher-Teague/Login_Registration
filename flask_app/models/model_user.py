##### Rename controller_"name" to reflect project #####

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash
from flask_app import app

from flask_bcrypt import Bcrypt

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

bcrypt = Bcrypt(app)

DATABASE_SCHEMA = 'login_and_reg'
##### RENAME: class_name(cap first letter), DATABASE_SCHEMA ##### 
##### table_name, column_name, all_table_name, new_table_name_id #####

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# C *************
# C *************
# C *************

    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        new_users_id = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

        return new_users_id

# R *************
# R *************
# R *************

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        all_users = []
        for users in results:
            all_users.append(User(users))
        return all_users

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) < 1:
            return False

        return User(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) < 1:
            return False

        return User(results[0])

# U *************
# U *************
# U *************

    # @classmethod
    # def update_one(cls, **data):
    #     query = 'UPDATE users SET column_name = %(coulmun_name)s WHERE id = %(id)s'
    #     return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

# D *************
# D *************
# D *************

    # @classmethod
    # def delete_one(cls, **data):
    #     query = 'DELETE FROM users WHERE id = %(id)s'
    #     connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
    #     return id


# ************* VALIDATIONS *************

    @staticmethod
    def validate_registration(post_data):
        is_valid = True

        if len(post_data['first_name']) < 2:
            flash ("First name must be at least 2 characters!")
            is_valid = False

        if len(post_data['last_name']) < 2:
            flash ("Last name must be at least 2 characters!")
            is_valid = False

        if not EMAIL_REGEX.match(post_data['email']):
            flash("invalid email address!")
            is_valid = False
        else:
            user = User.get_by_email({'email': post_data['email']})
            if user:
                flash("Email is already in use!")
                is_valid = False

        if post_data['password'] != post_data['confirm_password']:
            flash("Passwords do not match!")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(post_data):
        
        user = User.get_by_email({'email': post_data['email']})

        if not user:    
            flash ('User credentials are not valid!')
            return False 

        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash ('User credentials are not valid!')
            return False

        return True