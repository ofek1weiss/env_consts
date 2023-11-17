from typing import Callable, Optional, Type, TypeVar

from env_consts._env_consts_hot_loader import EnvConstsHotLoader
from env_consts._env_loader import EnvLoader

try:
    import dotenv  # type: ignore
except ImportError:
    dotenv = None

T = TypeVar("T")


def _set_env_values(cls, env_loader: EnvLoader):
    for attr, _type in cls.__annotations__.items():
        default_value = getattr(cls, attr, ...)
        value = env_loader.load(attr, _type, default_value)
        setattr(cls, attr, value)


def env_consts(
    cls=None,
    *,
    hotload: bool = False,
    prefix: Optional[str] = None,
    dotenv_path: Optional[str] = None
):
    """
    Decorator that loads environment variables into class attributes.

    Example:
        >>> @env_consts
        ... class Test:
        ...     TEST_INT: int = 0
        ...     TEST_STR: str = "default"
        >>> assert Test.TEST_INT == 0
        >>> assert Test.TEST_STR == "default"

    :param cls: Class to decorate.
    :param hotload: If True, the decorated class will be hot-loaded.
    :param prefix: Prefix for environment variables.
    :param dotenv_path: Path to dotenv file.
        (requires installation of python-dotenv)
    """
    if dotenv_path and not dotenv:
        raise RuntimeError("dotenv is not installed")
    default_env_values = (
        dotenv.dotenv_values(dotenv_path) if dotenv_path else None
    )
    env_loader = EnvLoader(
        prefix=prefix, default_env_values=default_env_values
    )

    def wrapper(cls):
        if not hotload:
            _set_env_values(cls, env_loader)
            return cls
        return EnvConstsHotLoader(cls, env_loader)

    if cls is None:
        return wrapper
    return wrapper(cls)


def set_type_converter(_type: Type[T], converter: Callable[[str], T]):
    """
    Set type converter for a specific type.

    Example:
        >>> set_type_converter(int, lambda x: int(x, base=16))

    :param _type: Type to convert.
    :param converter: Converter function.
    """
    EnvLoader.set_type_converter(_type, converter)
