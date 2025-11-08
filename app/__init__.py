from flask import Flask, render_template, flash, redirect, url_for, session, request, g
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user
from loguru import logger
import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config.get(config_name, config['default']))
    
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.users.models import User
        return User.get(int(user_id))
    
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)
    
    logger.add("app.log", rotation="500 MB", level="INFO")
    
    from app.users.views import users_bp
    from app.products.views import products_bp
    from app.views import main_bp
    from app.contact import contact_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(contact_bp, url_prefix='')
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal Server Error: {error}")
        return render_template('errors/500.html'), 500
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        from app.forms import ContactForm
        form = ContactForm()
        
        if form.validate_on_submit():
            try:
                log_message = (
                    f"New contact form submission:\\n"
                    f"Name: {form.name.data}\\n"
                    f"Email: {form.email.data}\\n"
                    f"Phone: {form.phone.data}\\n"
                    f"Subject: {form.subject.data}\\n"
                    f"Message: {form.message.data[:100]}..."
                )
                logger.info(log_message)
                
                flash(f"Повідомлення від {form.name.data} <{form.email.data}> успішно надіслано.", 'success')
                return redirect(url_for('contact'))
                
            except Exception as e:
                logger.error(f"Error processing contact form: {str(e)}")
                flash('Сталася помилка під час обробки форми. Спробуйте ще раз пізніше.', 'danger')
                return redirect(url_for('contact'))
        
        if form.is_submitted() and not form.validate():
            flash('Будь ласка, виправте помилки у формі та спробуйте ще раз.', 'warning')
            return redirect(url_for('contact'))
        
        return render_template('contact.html', form=form)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)