import os

import pytest

from env_consts._env_consts_hot_loader import EnvConstsHotLoader
from env_consts._env_loader import EnvLoader
from env_consts.errors import UnsetEnvironmentVariableError


def test_hot_load():
    class Test:
        TEST_INT: int
        TEST_STR: str = "default"

    test = EnvConstsHotLoader(Test, EnvLoader())
    assert test.TEST_STR == "default"
    with pytest.raises(UnsetEnvironmentVariableError):
        assert test.TEST_INT == 0

    os.environ["TEST_INT"] = "42"
    os.environ["TEST_STR"] = "42"
    assert test.TEST_INT == 42
    assert test.TEST_STR == "42"
