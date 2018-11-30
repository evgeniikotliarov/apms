from wsgiref import simple_server

from app_factory import AppFactory

application_factory = AppFactory()
application = application_factory.create_app()

if __name__ == '__main__':
    http_daemon = simple_server.make_server('0.0.0.0', 8000, application)
    http_daemon.serve_forever()
