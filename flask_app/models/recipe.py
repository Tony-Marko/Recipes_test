from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, request
from datetime import datetime
import re
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
db = 'recipes_schema'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.recipe = data['recipe']
        self.description = data['description']
        self.under_30 = data['under_30']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def add_recipe(cls, data):
        data = {
            'recipe' : request.form['recipe'],
            'description' : request.form['description'],
            'under_30' : request.form['under_30'],
            'instruction' : request.form['instruction'],
            'date_made' : request.form['date_made'],
            'user_id' : request.form['user_id']
        }
        query = """INSERT INTO recipes (recipe, description, under_30, instruction, date_made, user_id) 
                Values (%(recipe)s, %(description)s, %(under_30)s, %(instruction)s, %(date_made)s, %(user_id)s);"""
                    
                    # VALUES ('Test', 'Test', 'no', 'Test', '2022-05-29', '1');
        result = connectToMySQL(db).query_db(query, data)
        print("Recipe has been added as ID", result)

    @classmethod
    def edit_recipe(cls, data):
        data = {
            'id' : request.form['id'],
            'recipe' : request.form['recipe'],
            'description' : request.form['description'],
            'under_30' : request.form['under_30'],
            'instruction' : request.form['instruction'],
            'date_made' : request.form['date_made'],
        }
        query = """UPDATE recipes SET recipe = %(recipe)s, description = %(description)s, under_30 =%(under_30)s, instruction = %(instruction)s, date_made = %(date_made)s
        WHERE id = %(id)s; """
        result = connectToMySQL(db).query_db(query, data)
        print ("Recipe {result} has been updated")

    @classmethod
    def get_all_recipes(cls):
        query = """SELECT * FROM recipes;"""
        result = connectToMySQL(db).query_db(query)
        all_recipes = []
        for recipe in result:
            all_recipes.append(cls(recipe))
        # print("Get all result is", all_recipes)
        return all_recipes

    @classmethod
    def get_recipe_by_id(cls, id):
        data = { 'id' : id}
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def delete_recipe(cls, id):
        data = { 'id' : id}
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['recipe'])<3:
            flash("Recipe must have at least three characters")
            is_valid = False
        if len(data['description'])<3 or len(data['description'])>45:
            flash("Description must be at between 3 and 45 characters longer")
            is_valid = False
        if len(data['instruction'])<3:
            flash("Instructions must have at least three characters")
            is_valid = False
        if data['date_made'] == "":
            flash("Please select a date.")
            is_valid = False
        if 'under_30' not in data:
            flash("Please select if the recipe take longer than 30 minutes or not.")
            is_valid = False
        return is_valid

