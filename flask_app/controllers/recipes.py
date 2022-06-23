from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

from flask_app.models import user, recipe

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['post'])
def register():
    if user.User.validate_reg(request.form):
        data = user.User.parse_data(request.form)
        user_id = user.User.register(data)
        if user_id == False:
            flash("There was an error, please try again", 'error')
            return redirect ('/')
        session['user_id'] = user_id
        session['first_name'] = request.form['first_name']
        return redirect ('/dashboard')
    return redirect ('/')

@app.route('/login', methods = ['post'])
def login():
    data = {'email' : request.form['email']}
    user_indb = user.User.get_user_by_email(data)
    if not user_indb:
        flash("Invalid email/passord", "loginerror")
        return redirect ('/')
    if not bcrypt.check_password_hash(user_indb.password, request.form['password']):
        flash("Invalid email/passord", "loginerror")
        return redirect ('/')
    session['user_id'] = user_indb.id
    session['first_name'] = user_indb.first_name
    return redirect ('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log back in.", "loginerror")
        return redirect ('/')
    all_recipes = recipe.Recipe.get_all_recipes()
    return render_template ("dashboard.html", all_recipes = all_recipes)

@app.route('/create')
def create():
    if 'user_id' not in session:
        flash("Please log back in.", "loginerror")
    return render_template("create.html")

@app.route('/new_recipe', methods = ['post'])
def new_recipe():
    valid_data = recipe.Recipe.validate_recipe(request.form)
    if valid_data:
        add_recipe = recipe.Recipe.add_recipe(valid_data)
        return redirect ('/dashboard')
    return redirect ('/create')

@app.route('/edit/<id>')
def edit(id):
    if 'user_id' not in session:
        flash("Please log back in.", "loginerror")
        return redirect ('/')
    get_recipe = recipe.Recipe.get_recipe_by_id(id)
    yn = get_recipe.under_30
    session[yn] = "checked"
    return render_template('edit.html', get_recipe = get_recipe)

@app.route('/edit_recipe', methods = ['post'])
def edit_recipe():
    print(request.form)
    valid_data = recipe.Recipe.validate_recipe(request.form)
    print("Valid data is", valid_data)
    if valid_data:
        recipe.Recipe.edit_recipe(valid_data)
        return redirect ('/dashboard')
    new_page = f"/edit/{request.form['id']}"
    return redirect (new_page)

@app.route('/show/<id>')
def show_recipe(id):
    if 'user_id' not in session:
        flash("Please log back in.", "loginerror")
        return redirect ('/')
    get_recipe = recipe.Recipe.get_recipe_by_id(id)
    return render_template('show.html', get_recipe = get_recipe)

@app.route('/delete/<id>')
def delete_recipe(id):
    recipe.Recipe.delete_recipe(id)
    return redirect ('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
