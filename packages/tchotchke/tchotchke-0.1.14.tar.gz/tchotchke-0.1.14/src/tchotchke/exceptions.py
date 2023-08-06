class TchotchkeError(Exception):
    pass


class LoggableError(TchotchkeError):
    def __init__(self, message=None, log_sprinkles=None):
        super().__init__(message)
        self.log_sprinkles = log_sprinkles


class ConfigError(LoggableError):
    pass
