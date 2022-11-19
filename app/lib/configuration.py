#!/usr/bin/env python
from yaml import safe_load
from pathlib import Path
from lib.logger import logging
from sys import exit

log = logging.getLogger('config')


def configuration(prefix: str):
    try:
        filename = f'{prefix}.yml'

        if not Path(filename).is_file():
            filename = f'{prefix}.example.yml'
            log.warning(f'config file not found - using {filename}')

        configfile = open(filename, 'r')
        config = safe_load(configfile)
        configfile.close()
        log.info('configuration loaded successfully')
        return config

    except Exception:
        log.error(msg='unable to load configuration')
        exit(2)

