from flask_app import app
from flask_app import app
from flask import render_template, redirect, flash, request, session
from flask_app.models.recipe import Recipe


@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("add_recipe.html", userid=session['user_id'])


@app.route('/recipes/new/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect("/")
    if len(request.form['name']) < 3 or len(request.form['name']) > 45:
        flash("Name must be between 3-45 characters in length.", 'recipe1')
        return redirect('/recipes/new')
    if len(request.form['desc']) < 3 or len(request.form['desc']) > 75:
        flash("Description must be between 3-75 characters in length.", 'recipe2')
        return redirect('/recipes/new')
    if len(request.form['inst']) < 3 or len(request.form['inst']) > 255:
        flash("Instructions must be between 3-255 characters in length.", 'recipe3')
        return redirect('/recipes/new')
    if not request.form['date'] or request.form['date'] == "":
        flash("You must select a date.", 'recipe4')
        return redirect('/recipes/new')
    if 'under' not in request.form or request.form['under'] == "":
        flash("You must select whether the recipe is over/under 30 minutes.", 'recipe5')
        return redirect('/recipes/new')
    Recipe.create_new({
        "name": request.form['name'],
        "desc": request.form['desc'],
        "inst": request.form['inst'],
        "date": request.form['date'],
        "under": request.form['under'],
        "uid": session['user_id']
    })
    return redirect("/dashboard")


@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect("/")
    return render_template("show_recipe.html", userid=session['user_id'], firstname=session['first_name'], recipe=Recipe.get_by_id({"id": id}))


@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    recipe = Recipe.get_by_id({"id": id})
    if 'user_id' not in session:
        return redirect("/")
    print(int(session['user_id']))
    print(int(recipe.user_id))
    if int(session['user_id']) != int(recipe.user_id):
        return redirect("/dashboard")
    return render_template("edit_recipe.html", userid=session['user_id'], firstname=session['first_name'], recipe=recipe)


@app.route('/recipes/edit/<int:id>/confirm', methods=['POST'])
def confirm_edit_recipe(id):
    recipe = Recipe.get_by_id({"id": id})
    if 'user_id' not in session:
        return redirect("/")
    if int(session['user_id']) != int(recipe.user_id):
        return redirect("/dashboard")
    if len(request.form['name']) < 3 or len(request.form['name']) > 45:
        flash("Name must be between 3-45 characters in length.", 'recipe1')
        return redirect('/recipes/edit/' + str(id))
    if len(request.form['desc']) < 3 or len(request.form['desc']) > 75:
        flash("Description must be between 3-75 characters in length.", 'recipe2')
        return redirect('/recipes/edit/' + str(id))
    if len(request.form['inst']) < 3 or len(request.form['inst']) > 255:
        flash("Instructions must be between 3-255 characters in length.", 'recipe3')
        return redirect('/recipes/edit/' + str(id))
    if not request.form['date'] or request.form['date'] == "":
        flash("You must select a date.", 'recipe4')
        return redirect('/recipes/edit/' + str(id))
    if 'under' not in request.form or request.form['under'] == "":
        flash("You must select whether the recipe is over/under 30 minutes.", 'recipe5')
        return redirect('/recipes/edit/' + str(id))
    Recipe.edit({
        "name": request.form['name'],
        "desc": request.form['desc'],
        "inst": request.form['inst'],
        "date": request.form['date'],
        "under": request.form['under'],
        "id": id
    })
    return redirect('/dashboard')


@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect("/")
    if int(session['user_id']) != int(Recipe.get_by_id({"id": id}).user_id):
        return redirect("/dashboard")
    Recipe.delete({"id": id})
    return redirect('/dashboard')
