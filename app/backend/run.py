from wsgiref import simple_server

from tests.fake_app_factory import TestCopyOriginalAppFactory

application_factory = TestCopyOriginalAppFactory()
application = application_factory.create_app()

if __name__ == '__main__':
    http_daemon = simple_server.make_server('0.0.0.0', 8000, application)
    http_daemon.serve_forever()
