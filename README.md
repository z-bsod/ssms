# ssms

simple stupid monitoring system

this system has been built to run a bunch of simple checks (standard nagios plugins for the most part) on a small bunch of servers.

As most existing monitoring systems seem to be designed for monitoring a huge amount of checks on a large amount of servers they usually are complicated to setup, require a lot of configuration and seem to be overkill for this simple use case. SSMS tries to solve this issue in a simpler (and possibly stupid) way.

It consists of 2 components - the agent and the server

## the agent

the agent is the component running on the system which needs to be monitored. It's got a static yaml configuration file of the commands to run and in which interval these need to be run.

It runs one thread per check which alternatingly waits for the configured interval and runs the check command. The results of the checks are stored in memory and can be fetched via http as json.

### example configuration
```yaml
---
password: HttpBasicAuthPassword

defaults:
  interval: 120

checks:
  - name: SSL example.com
    command:
      - /usr/lib/nagios/plugins/check_ssl_cert
      - "-H"
      - example.com
      - "-P"
      - https
    nagios_check: True

  - name: apache running
    command:
      - /bin/systemctl
      - status
      - apache2.service
```

## the server

The server is running a simple status web interface and fetches the check results from all agents in the configured interval.
It's meant to do some alerting in the future as well but this hasn't been implemented yet.

### example configuration
```yaml
---
frontend_users:
  frontend_username: FrontendPassword

defaults:
  interval: 120
  password: HttpBasicAuthPassword

servers:
  - name: Example-Server 1
    url: http://exampleserver1:5001
  - name: Example-Server 2
    url: http://exampleserver2:5001
    interval: 30 # you can overwrite interval and password per server
    password: AnotherHttpAuthPassword
```