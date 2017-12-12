from threading import Thread


def start_thread(target, name):
    t = Thread(target=target)
    t.name = name
    t.daemon = True
    t.start()
    return t
