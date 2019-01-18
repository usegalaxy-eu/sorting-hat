# -*- coding: utf-8 -*-

import time

import flask
from flask import request
from statsd import StatsClient

__author__ = 'Chris Trotman'
__email__ = 'chris@trotman.io'
__version__ = '0.1.0'


class _StatsClient(StatsClient):
    def flask_time_start(self):
        if not hasattr(flask.g, 'extensions'):
            flask.g.extensions = {}

        flask.g.extensions.setdefault('stats', {})
        flask.g.extensions['stats'][self] = time.time()

    def flask_time_end(self, response):
        end_time = time.time()
        start_time = flask.g.extensions['stats'][self]

        total_time = end_time - start_time
        time_in_ms = total_time * 1000

        endpoint = str(request.endpoint)
        with self.pipeline() as pipeline:
            if request.endpoint is not None:
                pipeline.timing(endpoint, time_in_ms)

            pipeline.incr(
                '%s.http_%s' % (endpoint, response.status_code)
            )

        return response


class Stats(object):
    def __init__(self, app=None):
        if app:
            self.app = app
            self.client = self.init_app(app)
        else:
            self.app = None
            self.client = None

    def init_app(self, app):
        """Inititialise the extension with the app object.

        :param app: Your application object
        """
        host = app.config.get('STATS_HOSTNAME', 'localhost')
        port = app.config.get('STATS_PORT', 8125)
        base_key = app.config.get('STATS_BASE_KEY', app.name)

        client = _StatsClient(
            host=host,
            port=port,
            prefix=base_key,
        )

        app.before_request(client.flask_time_start)
        app.after_request(client.flask_time_end)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions.setdefault('stats', {})
        app.extensions['stats'][self] = client

        return client

    def __getattr__(self, name):
        return getattr(self.client, name, None)
