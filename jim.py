import doctest
import json

def bytes2msg(bytes):
    return json.loads(bytes.decode('utf8'))


def msg2bytes(msg):
    ''' Convert object to json bytes string
    >>> from jim import msg2bytes
    >>> msg2bytes('test')
    b'"test"'
    >>>
    '''
    return json.dumps(msg).encode('utf8')

doctest.testmod()