import time

from lib.logger import logging
from threading import Timer
from requests import get
log = logging.getLogger('checker')


class CheckServer:
    def fetch_server(self):
        self.last_request_started = time.asctime()
        log.debug(f'try to fetch data from {self.name}')
        try:
            r = get(
                self.url,
                auth=('monitoring', self.password),
                timeout=self.timeout
            )

            if r.status_code == 200:
                self.check_results = r.json()
                self.server_conn_result = "OK"
            elif 400 < r.status_code < 404:
                self.server_conn_result = "FORBIDDEN"
            elif r.status_code == 404:
                self.server_conn_result = "NOT FOUND"
            else:
                self.server_conn_result = f"Server Error: HTTP {r.status_code}"
            self.last_request_finished = time.asctime()

        except ConnectionError:
            log.error(f'error connecting to {self.name}')
            self.server_conn_result = "UNREACHABLE"

        except:
            log.error("something else went wrong")
            self.server_conn_result = "UNREACHABLE"

        self.timer = Timer(interval=self.interval, function=self.fetch_server)
        self.timer.daemon = True
        self.timer.start()

    def __init__(self, server, configuration):
        defaults = configuration.get('defaults')
        self.url = server['url']
        self.name = server['name']
        self.interval = server.get('interval', defaults.get('interval'))
        self.password = server.get('password', defaults.get('password'))
        self.timeout = server.get('timeout', defaults.get('timeout', 10))

        # initialize status variables
        self.timer = None
        self.last_request_started = None
        self.last_request_finished = None
        self.check_results = {}
        self.server_conn_result = "UNCHECKED"

        self.fetch_server()

    def get_values(self):
        values = {
            "name": self.name,
            "url": self.url,
            "server_conn_result": self.server_conn_result,
            "last_request_started": self.last_request_started,
            "last_request_finished": self.last_request_finished,
            "check_results": self.check_results.get('check_results')
        }
        return values


class ServerChecker:
    servers = []

    def __init__(self, configuration):
        servers = configuration.get('servers')
        for server in servers:
            log.debug(f"Monitoring {server.get('name')}")
            self.servers.append(CheckServer(
                server=server,
                configuration=configuration
            ))

    def get_data(self):
        server_values = []
        for server in self.servers:
            server_values.append(server.get_values())
        return server_values
