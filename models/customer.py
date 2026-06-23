from flask_login import UserMixin
from models import db
from extensions import bcrypt

class Customer(db.Model , UserMixin):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phno = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)

    bookings = db.relationship('Booking', backref='customer', lazy=True)
    
    def set_password(self, password):
        self.hashed_password = bcrypt.generate_password_hash((password).encode('utf-8')).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)
    
    def get_id(self):
        return str(self.customer_id)
    