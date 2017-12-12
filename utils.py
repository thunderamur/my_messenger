from threading import Thread


def start_thread(target, name, *args):
    t = Thread(target=target, *args)
    t.name = name
    t.daemon = True
    t.start()
    return t
