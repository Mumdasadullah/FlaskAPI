from extension import db
from datetime import datetime

class TimeStampedModel(db.Model):
    __abstract__ = True
    
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow())