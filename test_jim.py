import json
from jim import bytes2msg, msg2bytes


msg = 'test'
bytes = json.dumps(msg).encode('utf8')


def test_bytes2msg():
    assert bytes2msg(bytes) == msg


def test_msg2bytes():
    assert msg2bytes(msg) == bytes
