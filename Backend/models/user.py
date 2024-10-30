from extension import db
from models.base import TimeStampedModel
from sqlalchemy.ext.hybrid import hybrid_property
from extension import pwd_context


class User(TimeStampedModel):
    __tablename__ = "users"
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=50), nullable=False)
    father_name = db.Column(db.String(length=50))
    age = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    _password = db.Column("password", db.String(length=50), nullable=False)
    
    roles = db.relationship("Role", secondary="user_roles", back_populates="users")
    
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)
        
    def has_role(self, role):
        return bool(
            Role.query
            .join(Role.users)
            .filter(User.id == self.id)
            .filter(Role.slug == role)
            .count() == 1
        )
        
class Role(db.Model):
    __tablename__ = "roles"
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=50), nullable=False)
    slug = db.Column(db.String(length=50), nullable=False, unique=True)
    
    users = db.relationship("User", secondary="user_roles", back_populates="roles")
    
class UserRole(TimeStampedModel):
    __tablename__ = "user_roles"
    
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)