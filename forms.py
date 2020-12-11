"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, BooleanField
from wtforms.validators import InputRequired, Optional, URL


class AddPetForm(FlaskForm):
    """ Form for adding new Pet """

    name = StringField("Name", validators=[InputRequired()])
    species = SelectField("Species", 
                        choices=[
                            ("cat", "Cat"), 
                            ("dog", "Dog"), 
                            ("porcupine", "Porcupine")])
    photo_url = StringField("Pet Photo URL", validators=[Optional(), URL()])
    age = SelectField("Age",
                    choices=[
                        ("baby", "Baby"),
                        ("young", "Young"),
                        ("adult", "Adult"),
                        ("senior", "Senior")])
    notes = StringField("Notes", validators=[Optional()])


class EditPetForm(FlaskForm):
    """ Form for editing existing pet """

    photo_url = StringField("Pet Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes", validators=[Optional()])
    available = BooleanField("Available")


# Replaced RadioField with BooleanField
# choices=[ (True, "Available"), (False, "Not Available")]