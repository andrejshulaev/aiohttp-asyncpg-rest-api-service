import os
from app.utils import read_config, read_config_from_env


def test_config_validation(config):
    """Read and validate config files."""
    assert read_config(config.good_filepath)
    assert read_config(config.bad_filepath) is None

    os.environ['config_path'] = config.good_filepath
    assert read_config_from_env('config_path')

    os.environ['config_path'] = config.bad_filepath
    assert read_config_from_env('config_path') is None