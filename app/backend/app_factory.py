from app import App


class IAppFactory:
    def create_app(self):
        raise NotImplementedError()


class AppFactory(IAppFactory):
    def create_app(self):
        return App()
