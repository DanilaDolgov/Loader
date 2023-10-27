import typing

if typing.TYPE_CHECKING:
    from drive_server.app.base.application import Application


class BaseAccessor:
    config: typing.Any

    def __init__(self, app: 'Application'):
        self.app = app
        self._init_()

    def _init_(self) -> None:
        return



