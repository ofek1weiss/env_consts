class UnsetEnvironmentVariableError(ValueError):
    def __init__(self, env_name: str):
        self.env_name = env_name
        super().__init__(f"Environment variable {env_name} is not set")


class InvalidEnvironmentVariableError(ValueError):
    def __init__(self, env_name: str, _type: type):
        self.env_name = env_name
        self.type = _type
        super().__init__(
            f"Environment variable {env_name} is not of type {_type.__name__}"
        )
