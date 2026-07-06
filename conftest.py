"""Pytest configuration for test environment."""

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def disable_env_file():
    """Disable .env file loading and clear environment variables during tests."""
    env_file = ".env"
    env_backup = ".env.test_backup"

    # Save and clear CONVERSION_DIRECTORIES environment variable
    old_conv_dirs = os.environ.pop("CONVERSION_DIRECTORIES", None)

    # Rename .env if it exists
    if os.path.exists(env_file):
        os.rename(env_file, env_backup)

    yield

    # Restore .env after all tests
    if os.path.exists(env_backup):
        # Remove .env if it was created during tests
        if os.path.exists(env_file):
            os.remove(env_file)
        os.rename(env_backup, env_file)

    # Restore environment variable
    if old_conv_dirs is not None:
        os.environ["CONVERSION_DIRECTORIES"] = old_conv_dirs
