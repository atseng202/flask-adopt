"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.route("/")
def show_all_pets():
    """ List all the pets at root path """

    pets = Pet.query.all()
    return render_template("pets.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """ Add pet form; handle adding new pet """

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()

        return redirect("/")
    else:
        return render_template("form-new-pet.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def show_pet(pet_id):
    """ Show pet details page """

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()

        return redirect(f"/{pet_id}")
    else:
        return render_template('pet.html', form=form, pet=pet)

   