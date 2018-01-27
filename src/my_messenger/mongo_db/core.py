import time

from pymongo import MongoClient


"""
[
    {'to': to,
    'from': from,
    'messages': [
            {'time': time
            'message': message},
    ]},
]
"""


class MongoRepo:
    """Хранилище на MongoDB"""

    def __init__(self, host='localhost'):
        self.client = MongoClient(host)
        self.db = self.client.mm_client_db

    def push(self, from_, to, message):
        result = self.db.messages.update_one(
            {
                'from': from_,
                'to': to,
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
        if result.matched_count == 0:
            self.db.messages.insert(
                {
                    'from': from_,
                    'to': to,
                    'messages': [
                        {
                            'time': time.time(),
                            'message': message
                        }
                    ]
                }
            )

    def pop(self, from_=None, to=None):
        d = {}
        if from_:
            d.update({'from': from_})
        if to:
            d.update({'to': to})
        for msg in self.db.messages.find(d):
            self.db.messages.remove({'from': msg['from'], 'to': msg['to']})
            yield msg

    def get_all(self):
        for item in self.db.messages.find():
            yield item
