from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, current_user, logout_user
from .tools import email_format
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash(f'Welcome back {user.name}', category='ok')

                else:
                    flash('Email or password is incorrect', category='error')
            else:
                flash('Email or password is incorrect', category='error')





    return render_template('login.html', c_user=current_user)

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            repassword = request.form.get('repassword')

            if User.query.filter_by(email=email).first():flash('This email is already taken', category='error')
            elif len(name) < 3:flash('Name must be at least 3 characters long', category='error')
            elif not email_format(email):flash('Incorrect format for email', category='error')
            elif len(password) < 8:flash('Password must be at least 8 characters long', category='error')
            elif password != repassword:flash('Password did not match', category='error')
            else:
                new_user = User(name=name, email=email, password=generate_password_hash(password, method='scrypt'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True) # try remember=False

                flash('Account created', category='ok')
                return redirect(url_for('views.home'))
    return render_template('signup.html', c_user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))