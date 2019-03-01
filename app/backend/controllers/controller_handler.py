import falcon

from exceptions import BaseError, InvalidTokenError, TokenExpiredError, DeactivatedEmployeeError, \
    AuthenticationError
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
            token = _get_token(args[REQUEST])
            data = tokenizer.get_data_by_token(token)
            user_email, user_password = data['email'], data['password']
            args[CONTROLLER].user_email = user_email
            args[RESPONSE].status = falcon.HTTP_200
            controller(*args, **kwargs)
        except (TokenExpiredError,
                InvalidTokenError,
                AuthenticationError,
                DeactivatedEmployeeError) as error:
            args[RESPONSE].unset_cookie('token')
            args[RESPONSE].status = error.get_http_code()
        except BaseError as error:
            args[RESPONSE].status = error.get_http_code()

    def _get_token(request):
        token_from_header = request.headers['AUTHORIZATION'] if 'AUTHORIZATION' in request.headers \
            else None
        token_from_cookie = request.cookies['token'] if 'token' in request.cookies \
            else None
        token_attached = token_from_cookie or token_from_header
        if not token_attached:
            raise InvalidTokenError()
        token = token_from_header if token_from_header else token_from_cookie
        return token

    return wrap
