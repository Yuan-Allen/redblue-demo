class Server:
    def __init__(self, config: dict):
        self.config = config

    @classmethod
    def from_config(cls, config: dict):
        return cls(config)

    def run(self):
        raise NotImplementedError("TODO: Implement this functionality")
