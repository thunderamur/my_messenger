import json

def bytes2msg(bytes):
    return json.loads(bytes.decode('utf8'))


def msg2bytes(msg):
    return json.dumps(msg).encode('utf8')