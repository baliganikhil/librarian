from sqlalchemy import create_engine

from main import db

class BaseDAO(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # conn = None

    # def __init__(self):
    #     engine = create_engine('sqlite:///db/librarian.db', echo = True)
    #     self.conn = engine.connect()
    #     print('=== Connected to the database ===')

    def insert(self, ins):
        return self.conn.execute(ins)
