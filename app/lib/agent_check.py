import time
from threading import Timer
from subprocess import run
from lib.logger import logging

log = logging.getLogger('check')

class Check:
    def run_check(self):
        self.last_exec_start = time.asctime()
        log.debug(f'start command {self.command} at {self.last_exec_start}')
        try:
            runcheck = run(self.command, capture_output=True)

            # for nagios checks split text and perfdata
            perfdata = None
            if self.nagios_check:
                parts = runcheck.stdout.decode('utf-8').split('|')
                output_text = parts[0]
                perfdata = parts[1]
            else:
                output_text = runcheck.stdout.decode('utf-8')

            self.output = {
                "rc": runcheck.returncode,
                "stdout": runcheck.stdout.decode('utf-8'),
                "stderr": runcheck.stderr.decode('utf-8'),
                "output_text": output_text
            }
            if perfdata:
                self.output["perfdata"] = perfdata

            if runcheck.returncode == 0:
                self.state = "OK"
            elif runcheck.returncode == 1:
                self.state = "WARNING"
            else:
                self.state = "CRITICAL"
            self.last_exec_finish = time.asctime()
            log.debug(f'finished command {self.command} at {self.last_exec_start}')

        except:
            log.error(f'error trying to execute {self.command}')
            self.state = "CRITICAL"

        self.timer = Timer(interval=self.interval, function=self.run_check)
        self.timer.daemon = True
        self.timer.start()

    def __init__(self, configuration, check):
        defaults = configuration.get('defaults')
        self.name = check['name']
        self.command = check['command']
        self.nagios_check = check.get('nagios_check', False)
        self.interval = check.get('interval', defaults.get('interval', 300))

        # pre define variables for check output
        self.timer = None
        self.state = None
        self.output = {}
        self.last_exec_finish = None
        self.last_exec_start = None

        self.run_check()

    def get_values(self):
        values = {
            'name': self.name,
            'command': self.command,
            'last_exec_start': self.last_exec_start,
            'last_exec_finish': self.last_exec_finish,
            'output': self.output,
            'state': self.state
        }
        return values
