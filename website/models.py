from . import db
from flask_login import UserMixin
from .functions import get_datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # user id
    username = db.Column(db.String(100), unique=True) # unique - username must be unical
    email = db.Column(db.String)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=get_datetime()) # default - default value for this column
