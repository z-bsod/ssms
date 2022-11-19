#!/usr/bin/env python
import flask
from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from lib.logger import logging
from lib.configuration import configuration
from lib.server_checker import ServerChecker

log = logging.getLogger(name='server')
log.info('starting smss server')

config = configuration(prefix='config/server')
server = Flask(__name__)
auth = HTTPBasicAuth()
users = config.get('frontend_users')
serverchecker = ServerChecker(configuration=config)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(generate_password_hash(users.get(username)), password):
        return username


@server.route('/')
@auth.login_required
def index():
    output = flask.render_template(
        template_name_or_list='main.html.j2',
        servers=serverchecker.get_data()
    )
    return output


@server.route('/json')
@auth.login_required()
def show_json():
    server_data = {
        "servers": serverchecker.get_data()
    }
    return jsonify(server_data)


if __name__ == "__main__":
    server.run(host="0.0.0.0")
