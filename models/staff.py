from models import db
from extensions import bcrypt
from sqlalchemy import Enum

class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phno = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    experience = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(Enum('Available','On Holiday','Assigned','Inactive',name='staff_status'),nullable=False,default='Available')    
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    address = db.Column(db.String(100), nullable=False)

    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)

    treks = db.relationship('Trek', backref='assigned_staff', lazy=True)
    
    def set_password(self, password):
        self.hashed_password = bcrypt.generate_password_hash((password).encode('utf-8')).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)
    