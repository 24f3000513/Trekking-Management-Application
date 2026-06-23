from models import db
from extensions import bcrypt
from sqlalchemy import Enum

class Trek_Info(db.Model):
    __tablename__ = 'trek_info'

    trek_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(Enum('Easy','Moderate','Hard','Very Hard','Extreme',name='trek_difficulty'),nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    schedule = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    pickup_point = db.Column(db.String(100), nullable=False)
    drop_point = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(Enum('Open','Seasonally Closed','Permanently Closed','Blacklisted',name='trek_activity_status'),nullable=False,default='Open')
    bookings = db.relationship('Booking', backref='trek_info', lazy=True)
    images = db.relationship('Images', backref='trek_info', lazy=True)
    trek_slot = db.relationship('Trek_Slot',backref = 'trek_info',lazy = True)