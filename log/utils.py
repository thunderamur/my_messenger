class Log:

    def __init__(self, logger):
        self.logger = logger

    def __call__(self, func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            self.logger.debug('called')
            return result
        return inner