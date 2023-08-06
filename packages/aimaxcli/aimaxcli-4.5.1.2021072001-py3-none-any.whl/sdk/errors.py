import json

with open("errors.json") as fp:
    all_errors = json.load(fp)


class ClientException(Exception):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class NotSignedInException(ClientException):
    pass

