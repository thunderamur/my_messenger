"""
[
    {'to': to,
    'from': from,
    'messages': [
            {'time': time
            'message': message},
            {'time': time
            'message': message},
    ]},
    {'to': to,
    'from': from,
    'messages': [
            {'time': time
            'message': message},
    ]},
]
"""


import time

from pymongo import MongoClient


client = MongoClient('192.168.100.102')
db = client.mm_client_db


def insert():
    db.messages.insert(
        {
            'to': 'to',
            'from': 'from',
            'messages': [
                {
                    'time': time.time(),
                    'message': 'Some message is here...'
                }
            ]
        }
    )


dict_ = {
    'from': 'from',
}

dict_2 = {
    'to': 'to',
}

dict_3 = {
    'from': 'from',
    'to': 'to',
}



def update():
    db.messages.update(
        {
            'to': 'to',
            'from': 'from',
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


def drop():
    db.messages.drop()


def show():
    print('dict_')
    for msg in db.messages.find(dict_):
        print(msg)

    print('dict_2')
    for msg in db.messages.find(dict_):
        print(msg)

    print('dict_3')
    for msg in db.messages.find(dict_):
        print(msg)


cmd = ''


while cmd != 'q':
    cmd = input()
    if cmd == '1':
        insert()
    elif cmd == '2':
        update()
    elif cmd == '3':
        drop()
    elif cmd == '4':
        show()
