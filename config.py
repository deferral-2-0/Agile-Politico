import os

from dotenv import load_dotenv
load_dotenv()

"""
This contains our application configurations
"""


class Config:
    """
    This is the default configuration class
    Set Debug to False
    """
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URL')
    UPLOAD_DIR = os.getenv('UPLOAD_DIR')


class DevelopmentConfig(Config):
    """
    Our development configuration class
    Set Debug to True
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Our testing configuration class
    Set Debug to True
    """
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.getenv('DATABASE_TEST_URL')


"""
Declaring our application configuration
for development and testing
"""
app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
