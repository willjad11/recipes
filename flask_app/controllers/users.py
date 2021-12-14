from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, flash, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect("/dashboard")
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("dashboard.html", userid=session['user_id'], firstname=session['first_name'], recipes=Recipe.get_all())

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        redirect("/dashboard")
    if not User.validate_login(request.form):
        return redirect("/")
    return redirect("/dashboard")


@app.route('/logout', methods=['POST'])
def logout():
    if int(request.form['id']) == int(session['user_id']):
        session.clear()
    return redirect("/")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['pas'])
    user_id = User.register({
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "em": request.form['em'],
        "pas": pw_hash
    })
    session['user_id'] = user_id
    session['first_name'] = User.get_by_id({"id": user_id}).first_name
    session['last_name'] = User.get_by_id({"id": user_id}).last_name
    return redirect("/dashboard")
