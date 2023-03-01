from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)

# ===========  login and register view============
@app.route("/")
def index():
    return render_template("index.html")
#       register user     
@app.route("/users/register", methods=['post'])
def user_reg():
    print(request.form)
    if not User.validate(request.form):
        return redirect("/")
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        **request.form,
        'password' : pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id

    return redirect("/dashboard")
    #            dashboard page          
@app.route("/dashboard")
def dash():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        'id' : session['user_id']
    }
    # gett all recipes
    all_recipes = Recipe.get_all()
    logged_user = User.get_by_id(data)
    return render_template("welcome.html", logged_user=logged_user, all_recipes=all_recipes)
#------------login method post
@app.route("/users/login", methods=['post'])
def user_login():
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("invalid creds")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid creds")
        return redirect("/")
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")





#      logout       
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")