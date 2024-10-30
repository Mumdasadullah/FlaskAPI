from functools import wraps
from flask_jwt_extended import get_current_user
from flask import make_response, current_app as app
from extension import jwt
from models.user import User

@jwt.user_lookup_loader
def user_lookup(jwt_header, jwt_payload):
    user_id = jwt_payload.get(app.config.get("JWT_IDENTITY_CLAIM"))
    return User.query.filter_by(id=user_id).first()

def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_current_user()
            roles = role if isinstance(role, list) else [role]
            if all(not current_user.has_role(r) for r in roles):
                return make_response({"message": f"Missing any role in {' '.join(roles)}"}, 403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper