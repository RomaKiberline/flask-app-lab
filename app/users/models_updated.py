from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin):
    def __init__(self, id, username, email, password=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password) if password else None
        self.registered_on = datetime.utcnow()
        self.role = 'user'
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.country = None
        self.about_me = None
        self.last_seen = datetime.utcnow()
    
    def set_password(self, password):
        """Встановлення хешу пароля"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Перевірка пароля"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_seen(self):
        """Оновлення часу останнього візиту"""
        self.last_seen = datetime.utcnow()
    
    def get_full_name(self):
        """Повертає повне ім'я користувача"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def has_role(self, role_name):
        """Перевіряє, чи має користувач вказану роль"""
        return self.role == role_name
    
    def is_admin(self):
        """Перевіряє, чи є користувач адміністратором"""
        return self.role == 'admin'
    
    def to_dict(self):
        """Повертає дані користувача у вигляді словника"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'country': self.country,
            'about_me': self.about_me,
            'registered_on': self.registered_on.isoformat(),
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }
