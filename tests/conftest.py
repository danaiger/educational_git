import os
import pytest

from ugit import data


@pytest.fixture
def temp_dir(tmp_path):
    """Provides clean temp directory and sets GIT_DIR to it."""
    data.GIT_DIR = str(tmp_path / '.ugit')
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(old_cwd)


@pytest.fixture
def ugit_repo(temp_dir):
    """Initialized .ugit repo - calls data.init()"""
    data.init()
    return temp_dir
