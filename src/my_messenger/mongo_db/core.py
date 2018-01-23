import time

from pymongo import MongoClient


"""
[
    {'from': from,
     'to': [
                {'to': to,
                'messages': [
                        {'time': time
                        'message': message},
                        {'time': time
                        'message': message},
                ]},
                {'to': to,
                'messages': [
                        {'time': time
                        'message': message},
                ]},
    ]},
]
"""


class MongoRepo:
    """Хранилище на базе MongoDB"""

    def __init__(self, host='localhost'):
        self.client = MongoClient(host)
        self.db = self.client.mm_client_db

    def add(self, from_, to, message):
        self.db.messages.update(
            {
                'from': from_,
                'to': {
                    'to': to,
                }
            },
            {
                '$push': {
                    'messages': {
                        'time': time.time(),
                        'message': message
                    }
                }
            }
        )
