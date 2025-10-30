from flask import render_template, request, redirect, url_for
from app.users import users_bp

@users_bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', 'невідомо')
    return render_template('users/hi.html', name=name.upper(), age=age)

@users_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='Administrator', age=19))
