from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
import os
from .forms import RegistrationForm, LoginForm

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return render_template('index.html')

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        from . import db  # Import db within the function to avoid circular import
        from .models import User  # Import User model within the function
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        from .models import User  # Import User model within the function
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Replace with hashed password checking for production
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_blueprint.route('/dashboard')
@login_required
def dashboard():
    from .models import Task  # Import Task model within the function
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

@main_blueprint.route('/favicon.ico')
def favicon():
    """Serve the favicon when requested by the browser"""
    return send_from_directory(
        os.path.join(main_blueprint.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

