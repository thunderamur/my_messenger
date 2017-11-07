"""Константы для jim протокола, настройки"""
# Ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
RESPONSE = 'response'
ERROR = 'error'

# Значения
PRESENCE = 'presence'

RESPONSE_CODES = {
    100: 'basic_notice',
    200: 'ok',
    202: 'accepted',
    400: 'wrong_request',
    500: 'server_error'
}