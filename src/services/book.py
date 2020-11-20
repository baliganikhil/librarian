from services.baseService import BaseService
from daos.book import BookDAO

class BookService(BaseService):
    def get(self, bookId):
        r = BookDAO().get(bookId)
        return r

    def create(self, bookObj):
        return BookDAO().insert(bookObj)

    def update(self, bookId, bookObj):
        return BookDAO().update(bookId, bookObj)

    def delete(self, bookId):
        return BookDAO().delete(bookId)