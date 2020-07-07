import os
import configparser
# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']


config = configparser.ConfigParser()
basedir= os.path.abspath(os.curdir)
config.read(os.path.join(basedir,'config.ini'))
class Config:
    env=config
    JWT_SECRET_KEY = config.get('JWT', 'JWT_SECRET_KEY')
    JWT_REFRESH_TOKEN_EXPIRES=int(config['JWT']['JWT_REFRESH_TOKEN_EXPIRES'])
    JWT_ACCESS_TOKEN_EXPIRES=int(config['JWT']['JWT_ACCESS_TOKEN_EXPIRES'])
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.JWT_SECRET_KEY