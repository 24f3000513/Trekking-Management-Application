from flask import Flask, render_template, request
from config import Config
from models import db, Admin, Customer, Staff, Trek_Info, Trek_Slot, Booking, Images
from extensions import bcrypt, login_manager
from routes.auth import auth_bp
import utils.auth_helpers

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_bp)

def create_db():
    with app.app_context():
        db.create_all()
        print("Database created successfully.")
        existing_admin = Admin.query.filter_by(email=Config.ADMIN_EMAIL).first()
        if not existing_admin:
            admin = Admin(
                phno=Config.ADMIN_PHNO,
                email=Config.ADMIN_EMAIL
            )
            admin.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
            print("Default admin created successfully.")
        else: print("Admin already exists.")
create_db()


@app.route('/')
@app.route('/SherpaBuddy')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)