from src.utils.Constants import Constants
from src.utils.Utils import Utils


class ServerService:

    @classmethod
    def getLanguages(cls):
        languages = Constants.LANGUAGES
        return Utils.createSuccessResponse(True, languages)