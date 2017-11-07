import time

from client import MessengerClient

class TestMessengerClient(object):
    def setup(self):
        self.mc = MessengerClient()
        self.mc.set_user('name', 'status')

    def test_set_user(self):
        assert self.mc.user == {
            'account_name': 'name',
            'status': 'status'
        }

    def test_jim_presence(self):
        p = self.mc.jim_presence()
        assert p['action'] == 'presence'

    def test_jim_quit(self):
        assert self.mc.jim_quit() == {
            'action': 'quit'
        }