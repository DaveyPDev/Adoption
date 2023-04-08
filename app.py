from flask import Flask, render_template, redirect, flash, url_for, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "howboutnow123"

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["DEBUG"] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error_404.html', error=error), 404


@app.route('/')
def home():
    """Render pets page"""

    pets = Pet.query.all()
    return render_template("base.html", pets=pets)

@app.route('/animal_list')
def list_pets():
    """Render pets page"""

    pets = Pet.query.all()
    return render_template("pets_list.html", pets=pets)


@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """ Submit New Pet"""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        photo_url = form.photo_url.data
        species = form.species.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, photo_url=photo_url, species=species, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()

        flash('Pet added successfully')
        return redirect(url_for('list_pets'))

    elif request.method == "POST" and form.errors:
        if form.errors:
            flash("There were errors with your submission. Please fix them and try again.", "danger")
    return render_template("pet_add_form.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """ Edit Pet Info"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        print("Form SUBMITTED")
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data

        db.session.commit()

        flash('Pet updated successfully')
        return redirect(url_for('list_pets'))

    elif request.method == "POST" and form.errors:
        print(request.form)
        flash("There were errors with your edit submission. Please fix them and try again.", "danger")
    return render_template("pet_edit_form.html", form=form, pet=pet)

# @app.route('/<int:id>')
# def show_pet(id):
#     pet = Pet.query.get(id)
#     return render_template('show_pet.html', pet=pet)

@app.route("/api/pets/<int:pet_id>", methods=["GET"])
def api_get_pet(pet_id):

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
