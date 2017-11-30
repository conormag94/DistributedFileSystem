import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    FILES_FOLDER = '/tmp'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False