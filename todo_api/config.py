import os
from dotenv import load_dotenv


load_dotenv(".env")


# pylint: disable=invalid-name
class App_Config:
    """_summary_"""

    SECRET_KEY = os.getenv("SECRET_KEY", "test")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


    # SESSION CONFIG
    SESSION_TYPE = "filesystem" if not os.getenv("PROD", None) else "sqlalchemy"
    # SESSION_USE_SIGNER = True
    # SESSION_COOKIE_SECURE = False
    # SESSION_COOKIE_SAMESITE = "None"
    # SESSION_COOKIE_HTTPONLY = False
    # PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

    ## MAIL CONFIG
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("USER_MAIL")
    MAIL_PASSWORD = os.getenv("PASSWORD_MAIL")











