import json
import os
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from env_consts.errors import (
    InvalidEnvironmentVariableError,
    UnsetEnvironmentVariableError,
)

T = TypeVar("T")


class EnvLoader:
    _TYPE_CONVERTERS = {
        bool: lambda x: x.lower() in ("true", "1", "yes", "y"),
        list: json.loads,
        dict: json.loads,
        tuple: lambda x: tuple(json.loads(x)),
    }

    def __init__(
        self,
        prefix: Optional[str] = None,
        default_env_values: Optional[Dict[str, str]] = None,
    ):
        self.prefix = prefix
        self.default_env_values = default_env_values or {}

    @classmethod
    def get_type_converter(cls, _type: Type[T]) -> Callable[[str], T]:
        for converter_type, converter in cls._TYPE_CONVERTERS.items():
            if issubclass(_type, converter_type):
                return converter
        return _type

    @classmethod
    def set_type_converter(cls, _type: Type[T], converter: Callable[[str], T]):
        cls._TYPE_CONVERTERS[_type] = converter

    def _load_raw_value(self, env_name: str) -> Optional[str]:
        if env_name in os.environ:
            return os.environ[env_name]
        return self.default_env_values.get(env_name)

    def _parse_value(self, env_name: str, value: str, _type: Type[T]) -> T:
        converter = self.get_type_converter(_type)
        try:
            return converter(value)
        except Exception as e:
            raise InvalidEnvironmentVariableError(env_name, _type) from e

    def load(self, env_name: str, _type: Type[T], default: T = ...) -> Any:
        if self.prefix:
            env_name = self.prefix + env_name
        raw_value = self._load_raw_value(env_name)
        value = (
            self._parse_value(env_name, raw_value, _type)
            if raw_value is not None
            else default
        )
        if value is ...:
            raise UnsetEnvironmentVariableError(env_name)
        return value
