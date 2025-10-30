import os

class Config:
    """Базова конфігурація"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Конфігурація для розробки"""
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    """Конфігурація для тестування"""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Конфігурація для продакшену"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
