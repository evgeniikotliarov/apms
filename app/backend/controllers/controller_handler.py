import falcon

from exceptions import BaseError, InvalidTokenError
from utils.tokenizer import Tokenizer

CONTROLLER = 0
REQUEST = 1
RESPONSE = 2

tokenizer = Tokenizer()


def controller_handler(controller):
    def wrap(*args, **kwargs):
        try:
            args[RESPONSE].status = falcon.HTTP_200
            controller(*args, **kwargs)
        except BaseError as error:
            args[RESPONSE].status = error.get_http_code()

    return wrap


def authorized_controller_handler(controller):
    def wrap(*args, **kwargs):
        try:
            raw_token = args[REQUEST].headers['AUTHORIZATION']
            if not raw_token:
                raise InvalidTokenError()
            data = tokenizer.get_data_by_token(raw_token)
            user_email, user_password = data['email'], data['password']
            args[CONTROLLER].user_email = user_email
            args[RESPONSE].status = falcon.HTTP_200
            controller(*args, **kwargs)
        except BaseError as error:
            args[RESPONSE].status = error.get_http_code()

    return wrap
