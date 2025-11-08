from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from app.forms import ContactForm
import logging
from datetime import datetime

contact_bp = Blueprint('contact', __name__)

def setup_logger():
    logger = logging.getLogger('contact_form')
    logger.setLevel(logging.INFO)
    
    fh = logging.FileHandler('contact.log')
    fh.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(fh)
    
    return logger

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    logger = setup_logger()
    
    if form.validate_on_submit():
        try:
            log_message = (
                f"Contact Form Submission - Name: {form.name.data}, "
                f"Email: {form.email.data}, "
                f"Phone: {form.phone.data or 'Not provided'}, "
                f"Subject: {dict(form.subject.choices).get(form.subject.data)}, "
                f"Message: {form.message.data[:100]}..."
            )
            logger.info(log_message)
            
            flash(f'Дякуємо, {form.name.data}! Ваше повідомлення успішно надіслано.', 'success')
            
            return redirect(url_for('contact.contact'))
            
        except Exception as e:
            logger.error(f"Error processing contact form: {str(e)}")
            flash('Сталася помилка при обробці форми. Будь ласка, спробуйте ще раз пізніше.', 'danger')
    
    return render_template('contact.html', form=form)
