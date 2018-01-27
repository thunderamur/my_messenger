from .core import MongoRepo


repo = MongoRepo('192.168.100.102')


def drop():
    repo.db.messages.drop()


def show():
    for msg in repo.get_all():
        print(msg)


cmd = ''


while cmd != 'q':
    cmd = input()
    if cmd == '1':
        from_ = input('from: ')
        to = input('to: ')
        message = input('message: ')
        repo.push(from_, to, message)
    elif cmd == '2':
        from_ = input('from: ')
        to = input('to: ')
        for msg in repo.pop(from_, to):
            print(msg)
    elif cmd == '3':
        drop()
    elif cmd == '4':
        show()
