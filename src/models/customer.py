from sqlalchemy_serializer import SerializerMixin
from main import db

class Customers(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    mobile = db.Column(db.String(40))
    email = db.Column(db.String(40))
    address = db.Column(db.String(128))
    blacklisted = db.Column(db.String(10))
    regnum = db.Column(db.String(40))
    createdat = db.Column(db.DateTime(40))
    updatedat = db.Column(db.DateTime(40))
    createdby = db.Column(db.String(40))
    updatedby = db.Column(db.String(40))
    gender = db.Column(db.String(40))
    dob = db.Column(db.DateTime(40))