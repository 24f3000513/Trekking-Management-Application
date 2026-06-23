from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .admin import Admin
from .staff import Staff
from .customer import Customer
from .trek_info import Trek_Info
from .trek_slot import Trek_Slot
from .booking import Booking
from .image import Images