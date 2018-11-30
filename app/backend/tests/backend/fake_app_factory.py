from app import App
from app_factory import IAppFactory


class TestAppFactory(IAppFactory):
    def create_app(self):
        return App()
