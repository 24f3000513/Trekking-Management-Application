from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Admin, Customer, Staff
from forms import LoginForm, StaffRegistrationForm, CustomerRegistrationForm
from extensions import bcrypt
from utils.auth_helpers import redirect_by_role

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    
    form = LoginForm()
    if form.validate_on_submit():
        user_login_info = form.user_login_info.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = None
        role = None
        models = [Admin,Staff,Customer]

        for model in models:
            user = model.query.filter((model.email == user_login_info)|(model.phno == user_login_info)).first()
            if user:
                role = user.role
                break
        
        if user is None or not user.check_password(password):
            flash('Invalid email/phno or password','danger')
            return redirect(url_for('auth.login'))
        
        if role == 'staff':
            if user and user.is_blacklisted:
                flash('Staff is blacklisted, Contact Admin for more info','danger')
                return redirect(url_for('auth.login'))
            if user and not user.is_approved:
                flash('Staff is not approved yet, We contact you soon','danger')
                return redirect(url_for('auth.login'))
        if role == 'customer':
            if user and user.is_blacklisted:
                flash('Coustmer is blacklisted, Contact complaints@sherpabuddy.com for further queries','danger')
                return redirect(url_for('auth.login'))

        login_user(user, remember=remember_me)
        flash('Logged in successfully.', 'success')
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        
        if role == 'admin':
            return render_template('admin/dashboard')
        elif role == 'staff':
            return render_template('staff/dashboard')
        elif role == 'customer':
            return render_template('custmer/dashboard')
        return redirect(url_for('home'))       
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register/staff',methods = ['GET','POST'])
def register_staff():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    
    form = StaffRegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        phno = form.phone_number.data
        email = form.email.data.lower().strip()
        password = form.password.data
        experience = form.experience.data
        short_desc = form.short_description.data if form.short_description.data else None
        add = form.address.data

        staff = Staff(name = name, phno = phno, email = email, experience = experience, description = short_desc
                      ,status = 'Available', address= add)
        staff.set_password(password=password)

        db.session.add(staff)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Something Went Wrong','danger')        
        flash(
            f'Application Received! Your application was successful and is now awaiting admin approval. We will notify you via email once reviewed.',
            'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration_staff.html',form=form)

@auth_bp.route('/register/customer',methods = ['GET','POST'])
def register_customer():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        phno = form.phone_number.data
        email = form.email.data.lower().strip()
        password = form.password.data

        customer = Customer(name = name, phno = phno, email = email)
        customer.set_password(password=password)
        db.session.add(customer)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Something Went Wrong','danger')
        
        flash(f'Welcome to SherpaBuddy {customer.name}! Login and start exploring treks.','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration_customer.html',form=form)

@auth_bp.route('/logout',methods = ['GET', 'POST'])
@login_required
def logout():
    if current_user.role == 'admin':
        msg = "Chief Guide"
    elif current_user.role == 'staff':
        msg = f'Sherpa {current_user.name}'
    elif current_user.role == 'customer':
        msg = f'Wayfarer {current_user.name}'
    else:
        msg = "Explorer"
    logout_user()
    flash(f'Summit reached {msg}, See you soon!', 'success')
    return redirect(url_for('home'))