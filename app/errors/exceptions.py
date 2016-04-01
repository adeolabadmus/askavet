from werkzeug.exceptions import HTTPException


class AddNewQuestionException(HTTPException):
    code = 551