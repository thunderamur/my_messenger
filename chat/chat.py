class Chat(object):

    def __init__(self, client_1, client_2):
        self.clients = [client_1, client_2]
        self._data = {
            client_1: [],
            client_2: []
        }

    def put(self, client, message):
        self._data[client].append(message)

    def get(self, client):
        cli = self.clients[0]
        if cli == client:
            cli = self.clients[1]
        if len(self._data[cli]) > 0:
            return self._data[cli].pop(0)