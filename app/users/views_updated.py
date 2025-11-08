from flask import render_template, request, redirect, url_for, session, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.users import users_bp
from app.forms_updated import LoginForm, RegistrationForm
from functools import wraps
from datetime import datetime
import os

USERS = {}

class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()
        self.role = 'user'
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.country = None
        self.about_me = None
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

def init_users():

    admin = User(
        id=1,
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    admin.role = 'admin'
    admin.first_name = 'Admin'
    admin.last_name = 'System'
    admin.phone = '+380501234567'
    admin.country = 'Ukraine'
    admin.about_me = 'Системний адміністратор'
    
    USERS[admin.id] = admin
    
    user = User(
        id=2,
        username='user',
        email='user@example.com',
        password='password'
    )
    user.first_name = 'Іван'
    user.last_name = 'Петренко'
    user.phone = '+380671234567'
    user.country = 'Україна'
    user.about_me = 'Звичайний користувач системи'
    
    USERS[user.id] = user

init_users()

def get_user_by_username_or_email(identifier):
    for user in USERS.values():
        if user.username == identifier or user.email == identifier:
            return user
    return None

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Сторінка входу"""
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username_or_email(form.username.data)
        
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Вітаємо, {user.username}! Ви успішно увійшли до системи.', 'success')
            return redirect(next_page or url_for('users.profile'))
        else:
            flash('Невірне ім\'я користувача або пароль.', 'danger')
    
    return render_template('users/login.html', form=form)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Сторінка реєстрації"""
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = max(USERS.keys()) + 1 if USERS else 1
        user = User(
            id=user_id,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        
        USERS[user_id] = user
        login_user(user)
        flash(f'Вітаємо, {user.username}! Ваш акаунт успішно створено.', 'success')
        return redirect(url_for('users.profile'))
    
    return render_template('users/register.html', form=form)

@users_bp.route('/profile')
@login_required
def profile():
    """Сторінка профілю користувача"""
    return render_template('users/profile.html')

@users_bp.route('/logout')
@login_required
def logout():
    """Вихід з системи"""
    username = current_user.username
    logout_user()
    flash(f'До побачення, {username}! Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Редагування профілю користувача"""
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.phone = request.form.get('phone')
        current_user.country = request.form.get('country')
        current_user.about_me = request.form.get('about_me')
        
        flash('Профіль успішно оновлено!', 'success')
        return redirect(url_for('users.profile'))
    
    return render_template('users/edit_profile.html')

@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Зміна пароля"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if current_user.password != current_password:
            flash('Невірний поточний пароль', 'danger')
        elif new_password != confirm_password:
            flash('Новий пароль і підтвердження не співпадають', 'danger')
        else:
            current_user.password = new_password
            flash('Пароль успішно змінено!', 'success')
            return redirect(url_for('users.profile'))
    
    return render_template('users/change_password.html')
