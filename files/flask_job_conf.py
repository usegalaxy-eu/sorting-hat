#!/usr/bin/env python
import os
import sys
import yaml

# BEGIN MOCKS
sys.modules['galaxy'] = object()
# Mock the jobs / jobdestination class knowing it WILL NOT BE CALLED.
class jobs(object): # NOQA
    def JobDestination(*args, **kwargs):
        pass
sys.modules['galaxy.jobs'] = jobs # NOQA
# END MOCKS

# Back to code.
from flask import Flask, request, jsonify # NOQA
from job_conf import _gateway, name_it # NOQA

app = Flask(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'conf.yaml')

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as handle:
        APP_CONFIG = yaml.load(handle)

    if 'sentry_dsn' in APP_CONFIG:
        from raven.contrib.flask import Sentry
        sentry = Sentry(app, dsn=APP_CONFIG['sentry_dsn'])

    if 'statsd' in APP_CONFIG:
        app.config['STATS_HOSTNAME'] = APP_CONFIG['statsd']['host']
        app.config['STATS_PORT'] = APP_CONFIG['statsd']['port']
        app.config['STATS_BASE_KEY'] = APP_CONFIG['statsd']['prefix']

        from flask_stats import Stats
        stats = Stats().init_app(app)


@app.route('/', methods=['GET', 'POST'])
def gateway():
    if request.method != 'POST':
        return jsonify({})

    content = request.get_json()
    if not content:
        return jsonify({})

    if 'tool_id' not in content or 'user_roles' not in content \
            or 'email' not in content:
        return jsonify({})

    try:
        env, params, runner, spec = _gateway(content['tool_id'],
                                             content['user_roles'],
                                             content['email'])
        return jsonify({
            'env': env,
            'params': params,
            'runner': runner,
            'spec': spec,
        })
    except Exception as e:
        response = jsonify({'error': str(e)})
        response.status_code = 500
        return response


@app.route('/failure', methods=['GET', 'POST'])
def failure():
    raise Exception("Planned exception")


if __name__ == "__main__":
    app.run()
