from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, Optional, NumberRange

from grocery_app.models import GroceryStore, ItemCategory

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    title = StringField('Store Name', 
        validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Your title needs to be betweeen 3 and 80 characters")
        ])

    address = StringField('Store Address', 
        validators=[
            DataRequired(), 
            Length(min=5, max=200, message="Your address needs to be betweeen 3 and 200 characters")
        ])

    submit = SubmitField('Submit')


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    name = StringField('Item Name', 
        validators=[
            DataRequired(), 
            Length(min=1, max=80, message="Your name needs to be betweeen 3 and 80 characters")
        ])

    price = FloatField('Price ($)', 
        validators=[DataRequired(), NumberRange(min=0.01)])

    category = SelectField('Category', 
        choices=[(category.name, category.value) for category in ItemCategory])

    photo_url = StringField('Photo URL', 
        validators=[DataRequired()])

    store = QuerySelectField('Store',
        query_factory=lambda: GroceryStore.query.all(),
        get_label='title', 
        allow_blank=False)


    submit = SubmitField('Submit')