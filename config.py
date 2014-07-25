import os


class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SEND_FILE_MAX_AGE_DEFAULT = 60
  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
  DEBUG = False


class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True


class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True


class TestingConfig(Config):
  TESTING = True
