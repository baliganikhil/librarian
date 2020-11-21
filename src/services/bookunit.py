from services.baseService import BaseService
from daos.bookunit import BookunitDAO
from services.book import BookService

class BookunitService(BaseService):
    def get(self, bookunitId):
        r = BookunitDAO().get(bookunitId)
        return r

    def getByBarcode(self, barcode):
        r = BookunitDAO().getByBarcode(barcode)
        return r

    def create(self, bookunitObj):
        return BookunitDAO().insert(bookunitObj)

    def update(self, bookunitId, bookunitObj):
        return BookunitDAO().update(bookunitId, bookunitObj)

    def delete(self, bookunitId):
        return BookunitDAO().delete(bookunitId)

    def list(self, bookId):
        return BookunitDAO().list(bookId)

    def getBookByBookunitId(self, bookunitId):
        bookunit = self.get(bookunitId)
        bookId = bookunit.bookId
        return BookService().get(bookId)