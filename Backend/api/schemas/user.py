from extension import ma
from models.user import User
from marshmallow.fields import String
from marshmallow import ValidationError, validate, validates_schema

class UserSchema(ma.SQLAlchemyAutoSchema):
    name = String(required=True, validate=[validate.Length(min=3)], error_messages={
        "required": "Name is required",
        "invlaid": "Name should be string"
    })
    email = String(required=True, validate=[validate.Email()], error_messages={
        "required": "Email is required",
        "invalid": "Email should be string"
    })
    
    @validates_schema
    def email_check(self, data, **kwargs):
        email = data.get("email")
        
        if User.query.filter_by(email=email).count():
            raise ValidationError(f"Email {email} already exist")
    
    class Meta:
        model = User
        load_instance = True
        exclude = ["id", "_password"]
        
class UserCreateSchema(UserSchema):
    password = String(required=True, validate=[validate.Length(min=4)], error_messages={
        "required": "Password is required",
        "invalid": "Password should be string"
    })