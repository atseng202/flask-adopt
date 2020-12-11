"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, Length

AGE_CHOICES = [
    ("baby", "Baby"),
    ("young", "Young"),
    ("adult", "Adult"),
    ("senior", "Senior"),
]

SPECIES_CHOICES = [
    ("cat", "Cat"), 
    ("dog", "Dog"), 
    ("porcupine", "Porcupine")
]


class AddPetForm(FlaskForm):
    """ Form for adding new Pet """

    name = StringField("Name", validators=[InputRequired()])
    species = SelectField("Species", choices=SPECIES_CHOICES)
    photo_url = StringField("Pet Photo URL", validators=[Optional(), URL()])
    age = SelectField("Age", choices=AGE_CHOICES)

    # Note: add a length validation etc. if expecting certian info; Optional doesnt do anything alone
    notes = StringField("Notes", validators=[Optional(), Length(max=100)])


class EditPetForm(FlaskForm):
    """ Form for editing existing pet """

    photo_url = StringField("Pet Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes", validators=[Optional(), Length(max=100)])
    available = BooleanField("Available")
