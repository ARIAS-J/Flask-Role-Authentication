from os import name
from flask import Blueprint, render_template, redirect, request, url_for
from flask.helpers import flash
from .models import User, Role
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        
        
        
        user = User.query.filter_by(username=username).first()
        
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Success', category='success')
                login_user(user, remember=True)
                if current_user.has_roles('Admin'):
                    return redirect(url_for('views.view_admin'))
                else:
                    return redirect(url_for('views.view_guest'))
            else:
                flash('Incorrect Password.', category='error')
        else:
            flash('Username does not exists.', category='error')

    return render_template('login.html', username=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if request.method == 'POST':

        
        username = request.form.get('username')
        password = request.form.get('password')
        passwordconfirm = request.form.get('passwordconfirm')
        email = request.form.get('email')
        role = request.form.get('role')
        
        
        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists.', category='error')
        elif len(username) <= 1:
            flash('Username incorrecto.', category='error')
        elif len(password) < 6:
            flash('La contraseña es menor a 6 caracteres', category='error')
        elif password != passwordconfirm:
            flash('Contraseñas no coinciden.', category='error')

        else:
            # add to database
            new_user = User(username = username, password=generate_password_hash(password, method='sha256'), email = email)
            userrole = Role(name=role)

            new_user.roles = [userrole,]
            db.session.add(new_user)
            db.session.commit()

    
            flash('Account Created!', category='success')
            
            return redirect(url_for('views.view_home'))
        
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))