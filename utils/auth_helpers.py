from extensions import login_manager
from models import Admin, Customer, Staff
from flask import redirect, url_for, render_template


@login_manager.user_loader
def load_user(user_id):
    try:
        role, actual_id = user_id.split(":")
        if role == "admin":
            return Admin.query.get(int(actual_id))
        elif role == "staff":
            return Staff.query.get(int(actual_id))
        elif role == "customer":
            return Customer.query.get(int(actual_id))
    except ValueError:
        return None
    return None
    
def redirect_by_role(user):
    if user.role == 'admin':
        return render_template('admin/dashboard')

    elif user.role == 'staff':
        return redirect(url_for('staff.dashboard'))

    elif user.role == 'customer':
        return redirect(url_for('customer.dashboard'))

    return redirect(url_for('home'))