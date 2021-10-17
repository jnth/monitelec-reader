import logging
import logging.config
import os

import yaml

rootdir = os.path.dirname(os.path.abspath(__file__))


def configure_logs(verbose: bool, records_output: str):
    """Configure logger."""
    with open(os.path.join(rootdir, 'logging.yaml')) as f:
        config = yaml.safe_load(f.read())
        config['handlers']['console']['level'] = "DEBUG" if verbose else "INFO"
        config['handlers']['buffered_file']['filename'] = records_output
        logging.config.dictConfig(config)
