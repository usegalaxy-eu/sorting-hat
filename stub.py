from galaxy.jobs import JobDestination

import backoff
import json
import logging
import requests

log = logging.getLogger(__name__)


def name_it(tool_spec):
    if 'cores' in tool_spec:
        name = '%scores_%sG' % (tool_spec.get('cores', 1), tool_spec.get('mem', 4))
    elif len(tool_spec.keys()) == 0 or (len(tool_spec.keys()) == 1 and 'runner' in tool_spec):
        name = '%s_default' % tool_spec.get('runner', 'sge')
    else:
        name = '%sG_memory' % tool_spec.get('mem', 4)

    if tool_spec.get('tmp', None) == 'large':
        name += '_large'

    if 'name' in tool_spec:
        name += '_' + tool_spec['name']

    return name


@backoff.on_exception(backoff.fibo,
                      # Parent class of all requests exceptions, should catch
                      # everything.
                      requests.exceptions.RequestException,
                      # https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
                      jitter=backoff.full_jitter,
                      max_tries=8)
def _gateway2(tool_id, user_roles, user_email, memory_scale=1.0):
    payload = {
        'tool_id': tool_id,
        'user_roles': user_roles,
        'email': user_email,
    }
    r = requests.post('http://127.0.0.1:8090', data=json.dumps(payload), timeout=1, headers={'Content-Type': 'application/json'})
    data = r.json()
    return data['env'], data['params'], data['runner'], data['spec']


def gateway(tool_id, user, memory_scale=1.0):
    # And run it.
    if user:
        user_roles = [role.name for role in user.all_roles() if not role.deleted]
        email = user.email
    else:
        user_roles = []
        email = ''

    try:
        env, params, runner, spec = _gateway2(tool_id, user_roles, email, memory_scale=memory_scale)
    except requests.exceptions.RequestException:
        # We really failed, so fall back to old algo.
        env, params, runner, spec = _gateway(tool_id, user_roles, email, memory_scale=memory_scale)

    name = name_it(spec)
    return JobDestination(
        id=name,
        runner=runner,
        params=params,
        env=env,
        resubmit=[{
            'condition': 'any_failure',
            'destination': 'resubmit_gateway',
        }]
    )


if __name__ == '__main__':
    pass
