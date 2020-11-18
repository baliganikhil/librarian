from sqlalchemy import create_engine

class BaseDAO:
    conn = None

    def __init__(self):
        engine = create_engine('sqlite:///db/librarian.db', echo = True)
        self.conn = engine.connect()
        print('=== Connected to the database ===')
