from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class AddPetForm(FlaskForm):
    """ Form for new pet """

    name = StringField("Pet Name", validators=[InputRequired()])

    species = SelectField("Species", choices=[("dog", "Dog"), ("cat", "Cat"), ("bird", "Bird")])

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])

    age = IntegerField("Age", validators=[InputRequired(), NumberRange(min=0, max=30)])

    notes = TextAreaField("Notes", validators=[Optional(), Length(min=0, max=30)] )


class EditPetForm(FlaskForm):
    """ Pet editing Form"""

    photo_url = StringField("Photo URL",validators=[Optional(), URL()])

    notes = TextAreaField("Comments",validators=[Optional(), Length(min=0, max=60)])

    available = BooleanField("Available?")

    def validate_photo_url(form, field):
        if not field.data:
            raise ValidationError("URL Cannot be empty")