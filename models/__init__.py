from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .admin import Admin
from .staff import Staff
from .customer import Customer
from .trek import Trek
from .booking import Booking
from .image import Images