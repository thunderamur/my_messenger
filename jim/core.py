import time
import json
import copy
from .config import *


class TooLongError(Exception):
    """Ошибка когда наше поле длинее чем надо"""

    def __init__(self, name, value, max_length):
        """
        :param name: имя поля
        :param value: текущее значение
        :param max_length: максимальное значение
        """
        self.name = name
        self.value = value
        self.max_length = max_length

    def __str__(self):
        return '{}: {} to long (> {} simbols)'.format(self.name, self.value, self.max_length)


class MaxLengthField:
    """Дескриптор ограничивающий размер поля"""

    def __init__(self, name, max_length):
        """
        :param name: имя поля
        :param max_length: максимальная длина
        """
        self.max_length = max_length
        self.name = '_' + name

    def __set__(self, instance, value):
        # если длина поля больше максимального значения
        if len(value) > self.max_length:
            # вызываем ошибку
            raise TooLongError(self.name, value, self.max_length)
        # иначе записываем данные в поле
        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        # получаем данные поля
        return getattr(instance, self.name)


class Jim:
    def __bytes__(self):
        """Приведение объекта к байтам"""
        print('СЛОВАРЬ', self.__dict__)
        daction = self.__dict__
        jaction = json.dumps(daction)
        baction = jaction.encode(ENCODING)
        return baction

    @staticmethod
    def create_from_bytes(baction):
        """
        Наиболее важный метод создания jim объекта из байтов
        :param baction: входной набор байтов
        :return: объект иерархии jim
        """
        # TODO: добавить всевозможные проверки входных данных!
        # тут может быть первая ошибка
        jaction = baction.decode(ENCODING)
        jaction = json.loads(jaction)

        # для классов с дескрипторами атрибуты начинаются с _
        # поэтому их надо заменить на стандартные
        for k, v in copy.deepcopy(jaction).items():
            if k.startswith('_'):
                del jaction[k]
                jaction[k[1:]] = v
        # там должен быть либо response либо action
        if ACTION in jaction:
            # значит это действие
            action = jaction[ACTION]
            # действие должно быть действием из списка
            if action in ACTIONS:
                # в зависимости от действия создаем нужный объект
                # при создании тоже могут быть ошибки если что то криво передали - обработать
                # удаляем само действие из словаря, чтобы можно было удобнее передать параметры
                # для этого копируем словарь
                params = copy.deepcopy(jaction)
                # можем спокойно удалть действие
                del params[ACTION]
                # еще надо удалить время
                del params[TIME]
                if action == PRESENCE:
                    return JimPresence(**params)
                elif action == MSG:
                    return JimMessage(**params)
                elif action == JOIN:
                    return JimJoin(**params)
                elif action == LEAVE:
                    return JimLeave(**params)
                elif action == QUIT:
                    return JimQuit()
                else:
                    # сюда по логике никогда не должны попадать но для надежности лучше обработать
                    pass
            else:
                # что то не верно - обработать
                pass
        elif RESPONSE in jaction:
            # значит это ответ от сервера
            # создаем объект ответа - могуть быть ошибки
            return JimResponse(**jaction)
        else:
            # пришло что то не то
            # нужно обработать
            pass


class JimAction(Jim):
    # __slots__ = (ACTION, TIME) - со слотами не работает __dict__ - а он нам нужен для перевода в json

    def __init__(self, action):
        self.action = action
        self.time = time.time()


class JimPresence(JimAction):
    # Имя пользователя ограничено 25 символов - используем дескриптор
    account_name = MaxLengthField('account_name', USERNAME_MAX_LENGTH)

    # __slots__ = (ACTION, ACCOUNT_NAME, TIME) - дескриптор конфилктует со слотами


    def __init__(self, account_name):
        self.account_name = account_name
        super().__init__(PRESENCE)


class JimMessage(JimAction):
    # __slots__ = (ACTION, TIME, TO, FROM, MESSAGE)
    to = MaxLengthField('to', USERNAME_MAX_LENGTH)
    from_ = MaxLengthField('from_', USERNAME_MAX_LENGTH)
    message = MaxLengthField('message', MESSAGE_MAX_LENGTH)

    def __init__(self, to, from_, message):
        self.to = to
        self.from_ = from_
        self.message = message
        super().__init__(MSG)


class JimRoom(JimAction):
    # __slots__ = (ACTION, TIME, TO, FROM, MESSAGE)
    room = MaxLengthField('room', ROOMNAME_MAX_LENGTH)

    def __init__(self, room, action):
        self.room = room
        super().__init__(action)


class JimJoin(JimRoom):
    def __init__(self, room):
        super().__init__(room, JOIN)


class JimLeave(JimRoom):
    def __init__(self, room):
        super().__init__(room, LEAVE)


class JimQuit(JimAction):
    def __init__(self):
        super().__init__(QUIT)


class ResponseCodeError(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return 'Неверный код ответа {}'.format(self.code)


class ResponseField:
    def __init__(self, name):
        """
        :param name: имя поля
        """
        self.name = '_' + name

    def __set__(self, instance, value):
        # если значение кода не входит в список доступных котов
        if value not in RESPONSE_CODES:
            # вызываем ошибку
            raise ResponseCodeError(value)
        # иначе записываем данные в поле
        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        # получаем данные поля
        return getattr(instance, self.name)


class JimResponse(Jim):
    # __slots__ = (RESPONSE, ERROR, ALERT)
    # Используем дескриптор для поля ответ от сервера
    response = ResponseField('response')

    def __init__(self, response, error=None, alert=None):
        self.response = response
        self.error = error
        self.alert = alert