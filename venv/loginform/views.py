from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_user import roles_required
from .models import User

views = Blueprint('views', __name__)

@views.route('/')
def view_home():

    return render_template('home.html')

@views.route('/admin')
@login_required
@roles_required('Admin')
def view_admin():
    
    return render_template('admin.html')

@views.route('/guest')
@login_required
@roles_required('Guest')
def view_guest():
    
    return render_template('guest.html')