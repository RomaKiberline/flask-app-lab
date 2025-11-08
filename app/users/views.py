from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.users import users_bp
from app.forms import LoginForm, RegistrationForm
from app.users.models import User, USERS
from datetime import datetime

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Сторінка реєстрації"""
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = max(USERS.keys()) + 1 if USERS else 1
        user = User.create(
            id=user_id,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        login_user(user)
        flash(f'Вітаємо, {user.username}! Ваш акаунт успішно створено.', 'success')
        return redirect(url_for('users.profile'))
    
    return render_template('users/register.html', form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Сторінка входу"""
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data) or User.get_by_email(form.username.data)
        
        if user and user.check_password(form.password.data):
    
            login_user(user, remember=form.remember.data)
            user.update_last_seen()
        
            next_page = request.args.get('next')
            
            remember_msg = " (запам'ятовано)" if form.remember.data else ""
            flash(f'Вітаємо, {user.username}! Ви успішно увійшли до системи{remember_msg}.', 'success')
            
            return redirect(next_page or url_for('users.profile'))
        else:
        
            flash('Невірне ім\'я користувача або пароль.', 'danger')
            
    return render_template('users/login.html', form=form)

@users_bp.route('/logout')
@login_required
def logout():
    """Вихід з системи"""
    username = current_user.username
    logout_user()
    flash(f'До побачення, {username}! Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/profile')
@login_required
def profile():
    """Сторінка профілю користувача"""
    return render_template('users/profile.html')

@users_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Редагування профілю користувача"""
    from app.users.models import USERS
    
    if request.method == 'POST':
        try:
            current_user.first_name = request.form.get('first_name')
            current_user.last_name = request.form.get('last_name')
            current_user.phone = request.form.get('phone')
            current_user.country = request.form.get('country')
            current_user.about_me = request.form.get('about_me')
            
            USERS[current_user.id] = current_user
            
            flash('Профіль успішно оновлено!', 'success')
            return redirect(url_for('users.profile'))
        except Exception as e:
            flash(f'Сталася помилка при оновленні профілю: {str(e)}', 'danger')
    
    return render_template('users/edit_profile.html')

@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Зміна пароля"""
    from app.users.models import USERS
    
    if request.method == 'POST':
        try:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not current_user.check_password(current_password):
                flash('Невірний поточний пароль', 'danger')
            elif new_password != confirm_password:
                flash('Новий пароль і підтвердження не співпадають', 'danger')
            else:
                current_user.set_password(new_password)
            
                USERS[current_user.id] = current_user
                
                flash('Пароль успішно змінено!', 'success')
                return redirect(url_for('users.profile'))
        except Exception as e:
            flash(f'Сталася помилка при зміні пароля: {str(e)}', 'danger')
    
    return render_template('users/change_password.html')