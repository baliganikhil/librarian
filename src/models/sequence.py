from sqlalchemy_serializer import SerializerMixin
from main import db

class Sequences(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))
    value = db.Column(db.Integer())
