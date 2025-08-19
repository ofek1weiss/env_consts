import os
from pathlib import Path

import pytest

from env_consts import env_consts
from env_consts.errors import UnsetEnvironmentVariableError


def test_env_consts():
    @env_consts
    class Test:
        TEST_INT: int = 0
        TEST_STR: str = "default"

    assert Test.TEST_INT == 0
    assert Test.TEST_STR == "default"

    os.environ["TEST_INT"] = "42"
    os.environ["TEST_STR"] = "42"
    assert Test.TEST_INT == 0
    assert Test.TEST_STR == "default"


def test_env_consts_hotload():
    @env_consts(hotload=True)
    class Test:
        TEST_INT: int
        TEST_STR: str = "default"

    with pytest.raises(UnsetEnvironmentVariableError):
        assert Test.TEST_INT == 0
    assert Test.TEST_STR == "default"

    os.environ["TEST_INT"] = "42"
    os.environ["TEST_STR"] = "42"
    assert Test.TEST_INT == 42
    assert Test.TEST_STR == "42"


def test_env_consts_prefix():
    os.environ["PREFIX_TEST_INT"] = "42"
    os.environ["PREFIX_TEST_STR"] = "42"

    @env_consts(prefix="PREFIX_")
    class Test:
        TEST_INT: int
        TEST_STR: str = "default"

    assert Test.TEST_INT == 42
    assert Test.TEST_STR == "42"


def test_env_consts_dotenv():
    dotenv_path = Path(__file__).parent / ".env"

    @env_consts(dotenv_path=str(dotenv_path))
    class Test:
        TEST_INT: int
        TEST_STR: str = "default"

    assert Test.TEST_INT == 42
    assert Test.TEST_STR == "42"


def test_env_consts_dotenv_overwrite():
    dotenv_path = Path(__file__).parent / ".env"
    os.environ["TEST_INT"] = "0"

    @env_consts(dotenv_path=str(dotenv_path))
    class Test:
        TEST_INT: int
        TEST_STR: str = "default"

    assert Test.TEST_INT == 0
    assert Test.TEST_STR == "42"
