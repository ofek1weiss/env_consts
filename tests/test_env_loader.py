import os
from enum import Enum
from typing import Any

import pytest

from env_consts._env_loader import EnvLoader
from env_consts.errors import (
    InvalidEnvironmentVariableError,
    UnsetEnvironmentVariableError,
)


class ExampleEnum(Enum):
    A = "a"
    B = "b"
    C = "c"


@pytest.mark.parametrize(
    "env_name,env_value,_type,value",
    [
        ("TEST_BOOL", "true", bool, True),
        ("TEST_BOOL", "false", bool, False),
        ("TEST_BOOL", "1", bool, True),
        ("TEST_BOOL", "0", bool, False),
        ("TEST_BOOL", "yes", bool, True),
        ("TEST_BOOL", "no", bool, False),
        ("TEST_BOOL", "y", bool, True),
        ("TEST_BOOL", "n", bool, False),
        ("TEST_BOOL", "True", bool, True),
        ("TEST_BOOL", "False", bool, False),
        ("TEST_BOOL", "YES", bool, True),
        ("TEST_BOOL", "NO", bool, False),
        ("TEST_BOOL", "Y", bool, True),
        ("TEST_BOOL", "N", bool, False),
        ("TEST_BOOL", "TRUE", bool, True),
        ("TEST_BOOL", "FALSE", bool, False),
        ("TEST_INT", "42", int, 42),
        ("TEST_FLOAT", "42.42", float, 42.42),
        ("TEST_STR", "42", str, "42"),
        ("TEST_LIST", "[1, 2, 3]", list, [1, 2, 3]),
        ("TEST_DICT", '{"a": 1, "b": 2}', dict, {"a": 1, "b": 2}),
        ("TEST_TUPLE", "[1, 2, 3]", tuple, (1, 2, 3)),
        ("TEST_ENUM", "a", ExampleEnum, ExampleEnum.A),
    ],
)
def test_env_loader(env_name: str, env_value: str, _type: type, value: Any):
    os.environ[env_name] = env_value
    loader = EnvLoader()
    loaded_value = loader.load(env_name, _type)
    assert loaded_value == value


def test_default_value():
    loader = EnvLoader()
    loaded_value = loader.load("TEST_DEFAULT", str, "default")
    assert loaded_value == "default"


def test_unset_value():
    loader = EnvLoader()
    with pytest.raises(UnsetEnvironmentVariableError):
        loader.load("TEST_UNSET", str)


def test_invalid_value():
    os.environ["TEST_INVALID"] = "invalid"
    loader = EnvLoader()
    with pytest.raises(InvalidEnvironmentVariableError):
        loader.load("TEST_INVALID", int)


def test_prefix():
    os.environ["PREFIX_TEST_INT"] = "42"
    loader = EnvLoader(prefix="PREFIX_")
    loaded_value = loader.load("TEST_INT", int)
    assert loaded_value == 42


def test_set_type_converter():
    os.environ["TEST_INT"] = "42"
    loader = EnvLoader()
    loader.set_type_converter(int, lambda x: int(x) + 1)
    loaded_value = loader.load("TEST_INT", int)
    assert loaded_value == 43
