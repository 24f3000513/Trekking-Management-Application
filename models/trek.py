from models import db
from extensions import bcrypt
from sqlalchemy import Enum

class Trek(db.Model):
    __tablename__ = 'trek'

    trek_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(Enum('Easy','Moderate','Hard','Very Hard','Extreme',name='trek_difficulty'),nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    schedule = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)


    pickup_point = db.Column(db.String(100), nullable=False)
    drop_point = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    available_slots = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    
    status = db.Column(Enum('Upcoming','Ongoing','Completed',name='trek_status'),nullable=False,default='Upcoming')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(Enum('Open','Seasonally Closed','Permanently Closed','Blacklisted',name='trek_activity_status'),nullable=False,default='Open')

    bookings = db.relationship('Booking', backref='trek', lazy=True)
    images = db.relationship('Images', backref='trek', lazy=True)

    __table_args__ = (
        db.CheckConstraint('available_slots >= 0', name='non-negative_available_slots'),
        db.CheckConstraint('total_slots >= 0', name='non-negative_total_slots'),
        db.CheckConstraint('available_slots <= total_slots', name='check_slots_relationship'),
        db.CheckConstraint('end_date >= start_date', name='check_date_relationship'),
    )