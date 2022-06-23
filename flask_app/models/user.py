from flask_app.models import recipe
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
db = 'recipes_schema'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.all_recipes = []
        
    @classmethod
    def register(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        result = connectToMySQL(db).query_db(query,data)
        print ("Registered result is", result)
        return result

    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users Where email = %(email)s;"""
        result = connectToMySQL(db).query_db(query, data)
        if len(result)<1:
            return False
        print(cls(result[0]))
        return cls(result[0])

    @classmethod
    def get_recipes_by_id(cls, data):
        query = """SELECT * FROM recipes
                LEFT JOIN users on users.id = recipes.users_id
                WHERE recipe_users.id = %(users_id)s"""
        result = connectToMySQL(db).query_db(query,data)
        print("Get all results", result)
        users_recipes = cls(result[0])
        for db_row in result:
            recipe_data = {
                'id' : db_row['id'],
                'recipe' : db_row['recipe'],
                'description' : db_row['description'],
                'under_30' : db_row['under_30'],
                'instruction' : db_row['instruction'],
                'date_made' : db_row['date-made'],
                'users_id' : db_row['users_id']
            }
            users_recipes.all_recipes.append(recipe.Recipe(recipe_data))
        return users_recipes.all_recipes

    @staticmethod
    def validate_reg(data):
        is_valid = True
        if len(data['first_name'])<2:
            flash("First name must have at least two characters", "error")
            is_valid = False
        if len(data['last_name'])<2:
            flash("First name must have at least two characters", "error")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email/password", "error")
            is_valid = False
        if len(data['password'])<8:
            flash("Password must have at least eight characters", "error")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Password do not match. Please try again.", "error")
            is_valid = False
        return is_valid

    @staticmethod
    def parse_data(data):
        parsed_data= {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email']
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data