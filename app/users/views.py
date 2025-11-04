from flask import render_template, request, redirect, url_for, session, flash, make_response
from app.users import users_bp
from functools import wraps


USERS = {
    'admin': 'admin123',
    'user': 'password',
    'roman': 'roman123'
}

def login_required(f):
    """Декоратор для перевірки автентифікації"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Будь ласка, увійдіть в систему для доступу до цієї сторінки.', 'error')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function

@users_bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', 'невідомо')
    return render_template('users/hi.html', name=name.upper(), age=age)

@users_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='Administrator', age=19))

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Сторінка входу"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash(f'Ласкаво просимо, {username}!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Невірне ім\'я користувача або пароль.', 'error')
            return redirect(url_for('users.login'))
    
    return render_template('users/login.html')

@users_bp.route('/profile')
@login_required
def profile():
    """Сторінка профілю"""
    username = session.get('username')
    

    cookies = {}
    for key, value in request.cookies.items():
        if key not in ['session']:
            cookies[key] = value
    

    color_scheme = request.cookies.get('color_scheme', 'default')
    
    return render_template('users/profile.html', 
                         username=username, 
                         cookies=cookies,
                         color_scheme=color_scheme)

@users_bp.route('/logout')
@login_required
def logout():
    """Вихід з системи"""
    username = session.get('username')
    session.pop('username', None)
    flash(f'До побачення, {username}!', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/add-cookie', methods=['POST'])
@login_required
def add_cookie():
    """Додавання cookie"""
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = request.form.get('max_age', type=int)
    
    if not key or not value:
        flash('Ключ і значення не можуть бути порожніми.', 'error')
        return redirect(url_for('users.profile'))
    
    response = make_response(redirect(url_for('users.profile')))
    
    if max_age and max_age > 0:
        response.set_cookie(key, value, max_age=max_age)
        flash(f'Cookie "{key}" додано з терміном дії {max_age} секунд.', 'success')
    else:
        response.set_cookie(key, value)
        flash(f'Cookie "{key}" додано (сесійне).', 'success')
    
    return response

@users_bp.route('/delete-cookie/<key>')
@login_required
def delete_cookie(key):
    """Видалення окремого cookie"""
    response = make_response(redirect(url_for('users.profile')))
    response.delete_cookie(key)
    flash(f'Cookie "{key}" видалено.', 'success')
    return response

@users_bp.route('/delete-all-cookies')
@login_required
def delete_all_cookies():
    """Видалення всіх cookies (окрім системних)"""
    response = make_response(redirect(url_for('users.profile')))
    
    for key in request.cookies.keys():
        if key not in ['session']:
            response.delete_cookie(key)
    
    flash('Всі cookies видалено.', 'success')
    return response

@users_bp.route('/set-color-scheme/<scheme>')
@login_required
def set_color_scheme(scheme):
    """Встановлення кольорової схеми"""
    if scheme not in ['light', 'dark', 'default']:
        flash('Невірна кольорова схема.', 'error')
        return redirect(url_for('users.profile'))
    
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('color_scheme', scheme, max_age=60*60*24*365)
    flash(f'Кольорову схему змінено на "{scheme}".', 'success')
    return response
