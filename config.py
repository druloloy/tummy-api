import os

class BaseConfig:
    ROOT_PATH = '/api/v1'

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "postgresql://druloloy-psql:rageagainstthemachine@localhost:5432/tummy_local_flask"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") # get from env
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

config = {
    "local": LocalConfig,
    "prod": ProductionConfig
}