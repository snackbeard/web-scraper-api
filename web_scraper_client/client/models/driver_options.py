class DriverOptions:
    def __init__(self, user_agent: str, options: list[str] | None = None):
        if options is None:
            options = list()
        
        self._user_agent = user_agent
        self._options = options

    def __dict__(self):
        return {
            'user_agent': self._user_agent,
            'options': self._options
        }