import codecs
from flask import Flask, request, jsonify
import traceback
import logging
from pyeact import logger_formmater
import socket


class Server:
    pages = []
    app = None
    logger = None
    host = 'localhost'
    resolved_host = 'localhost'
    port = 7500

    def __init__(self, host='localhost', port=7500):
        self.host = host
        self.port = port
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        ch = logging.StreamHandler()
        ch.setFormatter(logger_formmater.CustomFormatter())
        self.logger.addHandler(ch)
        self.app = Flask('Pyeact server')
        self.resolved_host = socket.gethostbyname(socket.gethostname())
        self.app.route('/bridge.js')(self.bridge)
        self.app.route('/bridge_api', methods=["POST"])(self.bridge_route)

    @staticmethod
    def bridge():
        return codecs.open('./pyeact/resources/bridge.js').read()

    def bridge_route(self):
        if request.is_json:
            json = request.json
            function_name = json['name']
            function_args = json['args']
            for i in self.pages:
                for k, v in i.registered_functions.items():
                    if k == function_name:
                        return jsonify({'status': True, 'res': v(*function_args)})
        return jsonify({'status': False})

    def add_page(self, page):
        for i in page.routes:
            self.app.route(i)(lambda: self.render_page(i))
        self.pages.append(page)

    def render_page(self, route):
        self.logger.info(f"{route} accessed")
        try:
            for i in self.pages:
                for j in i.routes:
                    if route == j:
                        return i.render()
        except Exception:
            self.logger.error(f"raised on {route}\n{traceback.format_exc()}")

    def run_server(self):
        self.logger.warning("Use a wsgi server in production")
        self.app.run(self.host, self.port)
