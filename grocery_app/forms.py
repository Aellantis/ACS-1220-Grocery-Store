from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from grocery_app.models import GroceryStore, GroceryItem, ItemCategory, User
from grocery_app.extensions import db
from wtforms.validators import DataRequired, Length, URL, InputRequired, NumberRange, ValidationError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

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

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')