from sqlalchemy_serializer import SerializerMixin
from main import db

class Rentals(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    bookunitId = db.Column(db.Integer())
    customerId = db.Column(db.Integer())
    charge = db.Column(db.Integer())
    duedate = db.Column(db.DateTime(40))
    status = db.Column(db.String(40))
    comments = db.Column(db.Text())

    createdat = db.Column(db.DateTime(40))
    updatedat = db.Column(db.DateTime(40))
    createdby = db.Column(db.String(40))
    updatedby = db.Column(db.String(40))
    # bookunits = db.relationship('Bookunits', backref='books', lazy=True)
