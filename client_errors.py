class PresenceFail(Exception):
    pass

class AuthenticateFail(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return '{}: {}'.format(self.response['response'], self.response['error'])
