from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional, EqualTo, ValidationError

class ContactForm(FlaskForm):
    name = StringField('Ім\'я', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Ім'я має містити від 4 до 10 символів")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Email(message="Некоректний email")
    ])
    
    phone = StringField('Телефон', validators=[
        Regexp(r'^\+380\d{9}$', message="Номер повинен бути у форматі +380XXXXXXXXX")
    ])
    
    subject = SelectField('Тема', choices=[
        ('', 'Оберіть тему'),
        ('question', 'Питання'),
        ('feedback', 'Відгук'),
        ('support', 'Підтримка'),
        ('other', 'Інше')
    ], validators=[DataRequired(message="Будь ласка, оберіть тему")])
    
    message = TextAreaField('Повідомлення', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(max=500, message="Повідомлення не повинно перевищувати 500 символів")
    ])

class LoginForm(FlaskForm):
    username = StringField('Логін або Email', validators=[
        DataRequired(message="Це поле обов'язкове")
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Пароль має містити від 4 до 10 символів")
    ])
    
    remember = BooleanField('Запам\'ятати мене')

class RegistrationForm(FlaskForm):
    username = StringField('Логін', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=20, message="Логін має містити від 4 до 20 символів"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Логін має містити лише літери, цифри, крапки або підкреслення')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Email(message="Некоректний email")
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Пароль має містити від 4 до 10 символів"),
        EqualTo('confirm_password', message='Паролі не співпадають')
    ])
    
    confirm_password = PasswordField('Підтвердіть пароль', validators=[
        DataRequired(message="Це поле обов'язкове")
    ])
    
    def validate_username(self, field):
        if field.data.lower() == 'admin':
            raise ValidationError('Це ім\'я користувача зарезервовано.')
    
    def validate_email(self, field):
        if field.data.lower() == 'admin@example.com':
            raise ValidationError('Цей email вже використовується.')
