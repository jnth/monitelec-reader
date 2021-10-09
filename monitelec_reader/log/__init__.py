import logging
import logging.config
import os

import yaml

rootdir = os.path.dirname(os.path.abspath(__file__))


def configure_logs(verbose: bool):
    """Configure logger."""
    with open(os.path.join(rootdir, 'logging.yaml')) as f:
        config = yaml.safe_load(f.read())
        config['loggers']['monitelec']['level'] = "DEBUG" if verbose else "INFO"
        logging.config.dictConfig(config)
