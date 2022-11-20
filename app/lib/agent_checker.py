#!/usr/bin/env python
from lib.logger import logging
from lib.agent_check import Check

log = logging.getLogger('checker')


class Checker:
    checks = []

    def __init__(self, configuration):
        for check in configuration['checks']:
            log.debug(f"create check {check['name']}")
            self.checks.append(
                Check(
                    check=check,
                    configuration=configuration))

    def show_data(self):
        check_values = []
        for check in self.checks:
            check_values.append(check.get_values())
        return check_values
