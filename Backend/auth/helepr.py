from flask_jwt_extended import decode_token
from flask import current_app as app
from datetime import datetime
from models.auth import Token
from extension import db
from sqlalchemy.exc import NoResultFound

def add_token(encoded_token):
    decoded_token = decode_token(encoded_token)
    jti = decoded_token.get("jti")
    token_type = decoded_token.get("type")
    user_id = decoded_token.get(app.config.get("JWT_IDENTITY_CLAIM"))
    expires = datetime.fromtimestamp(decoded_token.get("exp"))
    
    token = Token(
        jti=jti,
        token_type=token_type,
        expires=expires,
        user_id=user_id
    )
    
    db.session.add(token)
    db.session.commit()
    
def revoke_token(token_jti, user_id):
    try:
        token = Token.query.filter_by(jti=token_jti, user_id=user_id).one()
        token.revoked_at = datetime.utcnow()
        db.session.commit()
    except NoResultFound:
        raise Exception(f"No Token Found with {token_jti}")
    
def is_token_revoked(jwt_payload):
    jti = jwt_payload.get("jti")
    user_id = jwt_payload.get(app.config.get("JWT_IDENTITY_CLAIM"))
    try:
        token =Token.query.filter_by(jti=jti, user_id=user_id).one()
        return token.revoked_at is not None
    except NoResultFound:
        raise Exception(f"No Token Found with {jti}")