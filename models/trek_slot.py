from models import db
from models import db
from extensions import bcrypt
from sqlalchemy import Enum

class Trek_Slot(db.Model):
    __tablename__ = 'trek_slot'

    slot_id = db.Column(db.Integer, primary_key=True)
    trek_id = db.Column(db.Integer,db.ForeignKey('trek_info.trek_id'),nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    price = db.Column(db.Float, nullable=False)

    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)

    assigned_staff_id = db.Column(db.Integer,db.ForeignKey('staff.staff_id'),nullable=True)
    status = db.Column(Enum('Upcoming','Ongoing','Completed',name='trek_status'),nullable=False,default='Upcoming')

    created_at = db.Column(db.DateTime,nullable=False,default=db.func.current_timestamp())

    bookings = db.relationship('Booking', backref='trek_slot', lazy=True)


    __table_args__ = (
        db.CheckConstraint('available_slots >= 0', name='non-negative_available_slots'),
        db.CheckConstraint('total_slots >= 0', name='non-negative_total_slots'),
        db.CheckConstraint('available_slots <= total_slots', name='check_slots_relationship'),
        db.CheckConstraint('end_date >= start_date', name='check_date_relationship'),
    )