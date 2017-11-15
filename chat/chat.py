class Chat(object):
    """
    Класс Чат - класс, обеспечивающий взаимодействие двух клиентов.
    """
    def __init__(self, client_1, client_2):
        self.__clients = [client_1, client_2]
        self.__data = {
            client_1: [],
            client_2: []
        }

    def put(self, client, message):
        self.__data[client].append(message)

    def get(self, client):
        cli = self.__clients[0]
        if cli == client:
            cli = self.__clients[1]
        if len(self.__data[cli]) > 0:
            return self.__data[cli].pop(0)


class ChatController(object):
    """
    Класс ЧатКонтроллер - класс, обеспечивающий передачу данных из Чата в ГрафическийЧат и обратно;
    обрабатывает события от пользователя (ввод данных, отправка сообщения).
    """
    pass
