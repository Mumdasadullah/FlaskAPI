from dotenv import load_dotenv
import os
from datetime import timedelta
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_TOKEN_LOCATION = ["headers"]
JWT_IDENTITY_CLAIM = "user_id"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)