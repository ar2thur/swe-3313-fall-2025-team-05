import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Uuid
from sqlalchemy import ForeignKey, Column
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import db


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    def set_password(self, raw_password: str):
        # Store a HASHED password in the password column.
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str):
        # Check a raw password against the stored hashed password.
        return check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f'User: {self.name}, ID: {self.id}'

class ShoppingCart(db.Model):
    __tablename__ ="shoppingcarts"
    id = Column(Uuid, primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_checked_out = Column(Boolean, nullable=False, default=False)
    date_checked_out = Column(DateTime, nullable=True, default=None)
    sub_total = Column(Integer, nullable=True, default=None)
    tax = Column(Integer, nullable=True, default=None)
    total_cost = Column(Integer, nullable=True, default=None)

    def __repr__(self):
        return f'ShoppingCart for {self.user_id}, total: {self.total_cost}'

class ShoppingCartItem(db.Model):
    __tablename__ = "shoppingcartitems"
    id = Column(Integer, primary_key=True)
    shopping_cart_id = Column(Uuid, ForeignKey('shoppingcarts.id'), nullable=False)
    inventory_item_id = Column(Integer, ForeignKey('inventoryitems.id'), nullable=False)
    added_to_cart = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'Shopping cart item: {self.id}, relates to inventory item: {self.inventory_item_id}'

class InventoryItem(db.Model):
    __tablename__ = "inventoryitems"
    id = Column(Integer, primary_key=True)
    is_available = Column(Boolean, nullable=False, default=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    category = Column(String, nullable=True)
    picture_path = Column(String, nullable=False, default="static/no_picture_added.png")

    def __repr__(self):
        return f'Inventory Item: {self.name}, cost: {self.cost}, picture at: {self.picture_path}'

class Logistics(db.Model):
    __tablename__ = "logistics"
    
    id = Column(Integer, primary_key=True)
    overnight_shipping = Column(Integer, nullable=False, default=2900)
    three_day_shipping = Column(Integer, nullable=False, default=1900)
    ground_shipping = Column(Integer, nullable=False, default=0)
    tax = Column(Integer, nullable=False, default=7)











