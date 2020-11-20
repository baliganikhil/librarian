from sqlalchemy_serializer import SerializerMixin
from main import db

class Books(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    isbn13 = db.Column(db.String(40))
    isbn10 = db.Column(db.String(40))
    isbn = db.Column(db.String(40))
    author = db.Column(db.String(40))
    publisher = db.Column(db.String(40))
    language = db.Column(db.String(40))
    binding = db.Column(db.String(40))
    numpages = db.Column(db.Integer())
    description = db.Column(db.String(40))
    charge = db.Column(db.Integer())
    rentduration = db.Column(db.Integer())
    createdat = db.Column(db.DateTime(40))
    updatedat = db.Column(db.DateTime(40))
    createdby = db.Column(db.String(40))
    updatedby = db.Column(db.String(40))