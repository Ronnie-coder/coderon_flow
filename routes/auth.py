from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models.user import User
from models.client import Client
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Try to find user in both User and Client tables
        user = User.query.filter_by(email=email).first()
        if not user:
            user = Client.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            if hasattr(user, 'is_admin') and user.is_admin:
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('client.dashboard'))
            
        flash('Invalid email or password')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))