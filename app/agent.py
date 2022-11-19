#!/usr/bin/env python

from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from lib.logger import logging
from lib.configuration import configuration
from lib.agent_checker import Checker

config = configuration(prefix='config/agent')
agent = Flask(__name__)
auth = HTTPBasicAuth()
checker = Checker(configuration=config)
log = logging.getLogger('agent')
monitoring_pw_hash = generate_password_hash(config['password'])


@auth.verify_password
def verify_password(username: str, password: str):
    if username == 'monitoring' and check_password_hash(monitoring_pw_hash, password):
        return username


@agent.route('/')
@auth.login_required
def index():
    output = {
        "check_results": checker.show_data()
    }
    return jsonify(output)


if __name__ == "__main__":
    agent.run(host='0.0.0.0', port=5001)
