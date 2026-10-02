"""
Authentication & Authorization Routes
Handles user registration, student & admin login, logout, and session lifecycle.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Password matching check
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html', name=name, email=email)

        success, message, user = AuthService.register_user(name, email, password, role='student')
        if not success:
            flash(message, 'warning' if 'already exists' in message else 'danger')
            if 'already exists' in message:
                return redirect(url_for('auth.login'))
            return render_template('auth/register.html', name=name, email=email)

        # Log in newly registered user
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['role'] = user.role

        flash('Registration successful! Please complete your academic profile.', 'success')
        return redirect(url_for('student.profile'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        success, message, user = AuthService.authenticate_user(email, password)
        if not success:
            flash(message, 'danger')
            return render_template('auth/login.html', email=email)

        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['role'] = user.role

        flash(f'Welcome back, {user.name}!', 'success')
        next_url = request.args.get('next')
        if next_url and next_url.startswith('/') and not next_url.startswith('//'):
            return redirect(next_url)

        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'user_id' in session and session.get('role') == 'admin':
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        success, message, user = AuthService.authenticate_user(email, password, required_role='admin')
        if not success:
            flash('Invalid administrator credentials.', 'danger')
            return render_template('admin/login.html', email=email)

        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['role'] = user.role

        flash('Welcome to Admin Control Panel.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/login.html')


@auth_bp.route('/logout')
def logout():
    user_role = session.get('role')
    session.clear()
    flash('You have been successfully logged out.', 'info')
    if user_role == 'admin':
        return redirect(url_for('auth.admin_login'))
    return redirect(url_for('auth.login'))
