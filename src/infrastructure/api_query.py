class ApiConfig:
    def __init__(self, url: str, port: str):
        self._url = url
        self._port = port

    @property
    def url(self):
        return self._url

    @property
    def port(self):
        return self._port
