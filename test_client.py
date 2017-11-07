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
