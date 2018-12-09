import falcon

from exceptions import BaseError


def controller_handler(controller):
    def wrap(*args, **kwargs):
        try:
            # TODO: not auth
            # if not auth(request):
            #     raise BadRequestError
            args[2].status = falcon.HTTP_200
            controller(*args, **kwargs)
        except BaseError as error:
            args[2].status = error.get_http_code()

    return wrap
