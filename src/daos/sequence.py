from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, DateTime, Date, Text
from flask_sqlalchemy import SQLAlchemy

from main import db
from daos.basedao import BaseDAO
from models.sequence import Sequences

meta = MetaData()

class SequenceDAO(BaseDAO):
    def __init__(self):
        super().__init__()

        print('Initialising sequence dao')

    def get(self, typeValue):
        sequence = Sequences.query.filter_by(type=typeValue).first()
        sequenceValue = sequence.value

        sequence.value = sequence.value + 1
        db.session.commit()

        return sequenceValue