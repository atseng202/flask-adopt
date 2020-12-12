"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
import requests

from project_secrets import CLIENT_ID, SECRET_KEY

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

PETFINDER_AUTH_PATH = "https://api.petfinder.com/v2/oauth2/token"

auth_token = None

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.route("/")
def show_all_pets():
    """ List all the pets at root path """

    pets = Pet.query.all()
    return render_template("show_pets.html", pets=pets)


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

        flash(f"Added {pet.name} the {pet.species}")
        return redirect("/")
    else:
        return render_template("add_pet_form.html", form=form)

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

        flash(f"{pet.name} updated!")
        return redirect(f"/{pet_id}")
    else:
        return render_template('show_pet.html', form=form, pet=pet)

#    Routes to authenticate with Petfinder API

@app.before_first_request
def refresh_credentials():
    """ Get token once and store it globally """
    global auth_token
    auth_token = update_auth_token_string()

def update_auth_token_string():
    """ Authenticates with Petfinder API for an OAuth token and returns it """

    resp = requests.post(PETFINDER_AUTH_PATH, data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": SECRET_KEY
    })


    return resp.json()["access_token"]