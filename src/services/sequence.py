from services.baseService import BaseService
from daos.sequence import SequenceDAO

class SequenceService(BaseService):
    def getRegnum(self):
        r = SequenceDAO().get('regnum')
        return r