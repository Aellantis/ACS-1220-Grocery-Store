from grocery_app.extensions import db
from grocery_app.utils import FormEnum
from flask_login import UserMixin


class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'


class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')


class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(db.String)
    store_id = db.Column(
        db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    shopping_list_items = db.relationship(
        'User', 
        secondary='user_shopping_list', 
        back_populates='shopping_list_users'
    )


# Define the association table before the User class that references it
user_shopping_list = db.Table('user_shopping_list',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('grocery_item.id'))
)


class User(UserMixin, db.Model):
    """User model for authentication and shopping lists."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  # Increased length for password hash
    
    shopping_list_users = db.relationship(
        'GroceryItem', 
        secondary='user_shopping_list', 
        back_populates='shopping_list_items'
    )
    
    def __repr__(self):
        return f'<User: {self.username}>'