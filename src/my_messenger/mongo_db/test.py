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


import time

from pymongo import MongoClient


client = MongoClient('192.168.100.102')
db = client.mm_client_db

db.messages.insert(
    {
        'from': 'from',
        'to': {
            'to': 'to',
            'messages': [
                {
                    'time': time.time(),
                    'message': 'Some message is here...'
                }
            ]
        }
    }
)

dict_ = {
    'from': 'from',
}

dict_2 = {
    'from': 'from',
    'to': {
        'to': 'to',
    }
}

db.messages.update(
    {
        'from': 'from',
        'to': {
            'to': 'to',
        }
    },
    {
        '$push': {
            'messages': {
                'time': time.time(),
                'message': 'Some message is here...'
            }
        }
    }
)

print('dict_')
for msg in db.messages.find(dict_):
    print(msg)

print('dict_2')
for msg in db.messages.find(dict_2):
    print(msg)

db.mm_client_db.drop()