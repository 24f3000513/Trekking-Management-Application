from models import db
from extensions import bcrypt

class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True)
    phno = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.hashed_password = bcrypt.generate_password_hash((password).encode('utf-8')).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)
    
    def __repr__(self):
        return f"Admin('{self.admin_id}', '{self.phno}', '{self.email}')"