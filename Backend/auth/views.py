from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from extension import db, pwd_context, jwt
from api.schemas.user import UserCreateSchema, UserSchema
from models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from auth.helepr import add_token, revoke_token, is_token_revoked
from flask_jwt_extended import jwt_required

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {"message": "Input should be JSON format"}, 400
    
    schema = UserCreateSchema()
    user = schema.load(request.json)
    
    db.session.add(user)
    db.session.commit()
    
    schema = UserSchema()
    return {"message": "User Created Successfully", "user": schema.dump(user)}

@auth_blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"message": "Input should be in JSON format"}, 400
    
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return {"message": "Emai and Password required"}, 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not pwd_context.verify(password, user.password):
        return {"message": "Invalid Credentials"}, 400
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token(access_token)
    add_token(refresh_token)
    return {"access token": access_token, "refresh token": refresh_token}, 200

@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    add_token(access_token)
    return {"access token": access_token}, 200

@auth_blueprint.route("/revoke-access", methods=["DELETE"])
@jwt_required()
def revoke_access():
    jti = get_jwt().get("jti")
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    
    return {"message": "Access Token Revoked"}, 200


@auth_blueprint.route("/revoke-refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh():
    jti = get_jwt().get("jti")
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    
    return {"message": "Refresh Token Revoked"}, 200

@jwt.token_in_blocklist_loader
def check_if_token_revoke(jwt_header, jwt_payload):
    try:
        return is_token_revoked(jwt_payload)
    except Exception:
        return True

@auth_blueprint.errorhandler(ValidationError)
def handle_marshmallow_auth_error(error):
    return jsonify(error.messages), 400