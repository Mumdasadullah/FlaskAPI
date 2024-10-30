from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
jwt = JWTManager()
cor = CORS()
migrate = Migrate()