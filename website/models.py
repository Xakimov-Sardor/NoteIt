from . import db
from .tools import get_time
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime(timezone=True), default=get_time())
    walls = db.relationship('Wall', backref='ufw', passive_deletes=True)

class Wall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime(timezone=True), default=get_time())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    notes = db.relationship('Note', backref='wfn', passive_deletes=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    text = db.Column(db.Text)
    date_created = db.Column(db.DateTime(timezone=True), default=get_time())
    wall_id = db.Column(db.Integer, db.ForeignKey('wall.id', ondelete='CASCADE'))