from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, SearchField,DateField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, NumberRange,Length
from models import db, Admin, Customer, Staff, Trek_Info, Trek_Slot, Booking, Images

Staff_Status_Choices = [('Available', 'Available'), 
                        ('On Holiday', 'On Holiday'), 
                        ('Assigned', 'Assigned'), 
                        ('Inactive', 'Inactive')]

Trek_difficulty_Choices = [('Easy', 'Easy'),
                           ('Moderate', 'Moderate'),
                           ('Hard', 'Hard'),
                           ('Very Hard', 'Very Hard'),
                           ('Extreme', 'Extreme')]

Trek_Slot_Status_Choices = [('Upcoming', 'Upcoming'),
                       ('Ongoing', 'Ongoing'),
                       ('Completed', 'Completed')]

Trek_Activity_Status_Choices = [('Open', 'Open'),
                               ('Seasonally Closed', 'Seasonally Closed'),
                               ('Permanently Closed', 'Permanently Closed'),
                               ('Blacklisted', 'Blacklisted')]

class LoginForm(FlaskForm):
        user_login_info = StringField('Phone Number or Email', validators=[DataRequired(message="Please enter your phone number or email address.")])
        password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
        remember_me = BooleanField('Remember Me')
        submit = SubmitField('Login')

class CustomerRegistrationForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Register')
        
        def validate_email(self,email):
                user = Customer.query.filter_by(email = email.data.lower()).first()
                if user:
                        raise ValidationError('email already exists')
        
        def validate_phone_number(self,phone_number):
                user = Customer.query.filter_by(phno = phone_number.data).first()
                if user:
                        raise ValidationError('phone number already exists')

class StaffRegistrationForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
        experience = IntegerField('Experience (in years)', validators=[DataRequired(), NumberRange(min=0, message="Experience must be a non-negative number.")])
        short_description = TextAreaField('Short Description', validators=[Optional(), Length(max=500)])
        address = StringField('Address', validators=[DataRequired(), Length(min=5, max=100)])
        submit = SubmitField('Register')

        def validate_email(self,email):
                staff = Staff.query.filter_by(email = email.data.lower()).first()
                if staff:
                        raise ValidationError('email already exists')
        
        def validate_phone_number(self,phone_number):
                staff = Staff.query.filter_by(phno = phone_number.data).first()
                if staff:
                        raise ValidationError('phone number already exists')

class StaffProfileUpdateForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
        experience = IntegerField('Experience (in years)', validators=[DataRequired(), NumberRange(min=0, message="Experience must be a non-negative number.")])
        short_description = TextAreaField('Short Description', validators=[Optional(), Length(max=500)])
        address = StringField('Address', validators=[DataRequired(), Length(min=5, max=100)])
        submit = SubmitField('Update Profile')

class CustomerProfileUpdateForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
        submit = SubmitField('Update Profile')

class StaffStatusUpdateForm(FlaskForm):
        status = SelectField('Status', choices=Staff_Status_Choices, validators=[DataRequired()])
        submit = SubmitField('Update Status')

class StaffSearchForm(FlaskForm):
        search_query = SearchField('Search Staff', validators=[Optional(), Length(max=100)])
        submit = SubmitField('Search')

class CustomerSearchForm(FlaskForm):
        search_query = SearchField('Search Customer', validators=[Optional(), Length(max=100)])
        submit = SubmitField('Search')

class AddTrek(FlaskForm):
        trek_name = StringField('Trek Name', validators=[DataRequired(), Length(min=2, max=100)])
        description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
        location = StringField('Location', validators=[DataRequired(), Length(min=2, max=100)])
        difficulty = SelectField('Difficulty', choices=Trek_difficulty_Choices, validators=[DataRequired()])
        duration = IntegerField('Duration (in days)', validators=[DataRequired(), NumberRange(min=1, message="Duration must be at least 1 day.")])
        schedule = TextAreaField('Schedule', validators=[DataRequired(), Length(max=1000)])
        pickup_point = StringField('Pickup Point', validators=[DataRequired(), Length(min=2, max=100)])
        drop_point = StringField('Drop Point', validators=[DataRequired(), Length(min=2, max=100)])
        submit = SubmitField('Save Trek')

        def validate_trek_name(self,trek_name):
               trek = Trek_Info.query.filter_by(trek_name = trek_name.data).first()
               if trek:
                      raise ValidationError('Trek already exists')

class TrekActivityUpdateForm(FlaskForm):
    activity_status = SelectField('Activity Status',choices=Trek_Activity_Status_Choices,validators=[DataRequired()])
    submit = SubmitField('Update Status')

class AddImageForm(FlaskForm):
    image = FileField('Trek Image',validators=[DataRequired(),FileAllowed(['png', 'jpg', 'jpeg'],'Only PNG, JPG and JPEG files are allowed.')])
    submit = SubmitField('Upload')

class DeleteImageForm(FlaskForm):
    submit = SubmitField('Delete')

class AddSlotForm(FlaskForm):
    start_date = DateField('Start Date',validators=[DataRequired()])
    end_date = DateField('End Date',validators=[DataRequired()])
    price = FloatField('Price',validators=[DataRequired(),NumberRange(min=0,message="Price must be non-negative.")])
    total_slots = IntegerField('Total Slots',validators=[DataRequired(),NumberRange(min=1,message="Total slots must be at least 1.")])
    available_slots = IntegerField('Available Slots',validators=[DataRequired(),NumberRange(min=0,message="Available slots cannot be negative.")])
    assigned_staff_id = SelectField('Assigned Staff',coerce=int,validators=[Optional()])
    status = SelectField('Status',choices=Trek_Slot_Status_Choices,validators=[DataRequired()])
    submit = SubmitField('Add Slot')

    def validate_available_slots(self, field):
        if field.data > self.total_slots.data:
            raise ValidationError('Available slots cannot exceed total slots.')

    def validate_end_date(self, field):
        if field.data < self.start_date.data:
            raise ValidationError('End date cannot be before start date.')
        
class UpdateSlotStatusForm(FlaskForm):
      status = SelectField('Status',choices=Trek_Slot_Status_Choices,validators=[DataRequired()])
      submit = SubmitField('Update Status')

class BookingForm(FlaskForm):
    no_of_people = IntegerField('Number of People',validators=[DataRequired(),NumberRange(min=1,message="Atleat a person required to book")])
    submit = SubmitField('Confirm Booking')