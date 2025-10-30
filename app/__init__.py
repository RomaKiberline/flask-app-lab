from flask import Flask, render_template
import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config.get(config_name, config['default']))

    from app.users.views import users_bp
    from app.products.views import products_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')

    @app.route('/')
    def home():
        return render_template('index.html')

    return app

app = create_app()
