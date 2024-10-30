from flask_restful import Resource
from flask import request
from models.user import User
from api.schemas.user import UserSchema
from extension import db
from flask_jwt_extended import jwt_required
from auth.decorator import auth_role

class UserList(Resource):
    method_decorators = [auth_role("admin"), jwt_required()]
    def get(self):
        name_filter = request.args.get("name")
        age_filter = request.args.get("age")
        email_filter = request.args.get("email")
        sorts = request.args.get("sort")
        user_query = User.query
        if name_filter:
            user_query = user_query.filter(User.name.ilike(f"%{name_filter}%"))
        if age_filter:
            user_query = user_query.filter(User.age == age_filter)
        if email_filter:
            user_query = user_query.filter(User.email.in_(email_filter.split(',')))
        if sorts:
            for sort in sorts.split(','):
                field = getattr(User, sort)
                user_query = user_query.order_by(field)
        users = user_query.all()
        schema = UserSchema(many=True)
        return {"result": schema.dump(users)}
    
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        schema = UserSchema()
        return {"result": schema.dump(user)}
    
    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)
        
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User updated successfully", "user": schema.dump(user)}
    
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        schema = UserSchema()
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "User Deleted Successfully", "user": schema.dump(user)}