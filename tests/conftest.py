import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def starting_env():
    return os.environ.copy()


@pytest.fixture(autouse=True)
def reset_env(starting_env):
    os.environ.clear()
    os.environ.update(starting_env)
