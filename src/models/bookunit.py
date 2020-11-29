from sqlalchemy_serializer import SerializerMixin
from main import db

class Bookunits(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(40))
    bookId = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    createdat = db.Column(db.DateTime(40))
    updatedat = db.Column(db.DateTime(40))
    createdby = db.Column(db.String(40))
    updatedby = db.Column(db.String(40))