from sqlalchemy_serializer import SerializerMixin
from main import db

class BaseModel(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)