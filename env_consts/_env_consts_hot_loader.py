from typing import Any

from env_consts._env_loader import EnvLoader


class EnvConstsHotLoader:
    def __init__(self, cls: type, env_loader: EnvLoader):
        self._annotations = cls.__annotations__
        self._default_values = vars(cls)
        self._env_loader = env_loader

    def __getattr__(self, name: str) -> Any:
        if name not in self._annotations:
            raise AttributeError(name)
        _type = self._annotations[name]
        default = self._default_values.get(name, ...)
        return self._env_loader.load(name, _type, default)
