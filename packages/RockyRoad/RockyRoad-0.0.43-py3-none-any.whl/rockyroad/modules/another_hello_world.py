from .setup import *


@headers({"Ocp-Apim-Subscription-Key": key})
class AnotherHelloWorld(Consumer):
    def __init__(self, Resource, *args, **kw):
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @get("")
    def list(self):
        """This call will return Hello World."""