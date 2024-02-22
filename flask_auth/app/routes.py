from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from __init__ import login_manager
from .models import User, db
from .forms import LoginForm, SignupForm
from werkzeug.security import check_password_hash, generate_password_hash

users = Blueprint('users', __name__)
users_list = []


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@users.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=current_user)
    return redirect(url_for('users.login'))


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('users.index'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash('User already exists', 'error')
        else:
            new_user = User(email=email, password=generate_password_hash(password), name=name)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('users.login'))

    return render_template('signup.html', title='Sign Up', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
