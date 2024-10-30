from extension import db

class Token(db.Model):
    __tablename__ = "tokens"
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    jti = db.Column(db.String(length=30), nullable=False, unique=True)
    token_type = db.Column(db.String(length=10), nullable=False)
    revoked_at = db.Column(db.DateTime())
    expires = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False, index=True)
    
    users = db.relationship("User")