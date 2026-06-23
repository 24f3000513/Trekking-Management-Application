from models import db
from extensions import bcrypt
from sqlalchemy import Enum

class Booking(db.Model):
    __tablename__ = 'booking'

    booking_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek_info.trek_id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(Enum('Booked','Completed','Cancelled','Refunded',name='booking_status'),nullable=False,default='Booked')
    
    no_of_people = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    is_cancelled = db.Column(db.Boolean, nullable=False, default=False)
    refund_status = db.Column(db.Boolean, nullable=False, default=False)
    refund_amount = db.Column(db.Float, nullable=True)
    cancellation_date = db.Column(db.DateTime, nullable=True)
    cancellation_reason = db.Column(db.String(255), nullable=True)
