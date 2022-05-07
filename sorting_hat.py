#!/usr/bin/env python
# usegalaxy.eu sorting hat
"""

                                   .'lddc,.
                                'cxOOOOOOOOOxoc;,...
                            .:dOOOOOOOOOOOOOOOOOOOOOOOl
                        .;dOOOOOOOOOOOOOOxcdOOOOOOOkl.
                       oOOOOOOOOOOOOOOOx,    ......
                     .xOOkkkOOOOOOOOOk'
                    .xOOkkkOOOOOOOOO00.
                    dOOkkkOOOOOOOOOOOOd
                   cOOkkkOOOOOOOOOOOOOO'
                  .OOOkkOOOOOOOOOOOOOOOd
                  dOOkkOOOOOOOOOOOOOOOOO,
                 .OOOOOOOOOOOOOOOOOOOOOOx
                 cOOOOOOOOOOOOOOOOOOOOOOO;
                 kOOOOOOOxddddddddxOOOOOOk.
        ..,:cldxdlodxxkkO;'''''''';Okkxxdookxdlc:,..
   .;lxO00000000d;;;;;;;;,'';;;;'',;;;;;;;:k00000000Oxl;.
  d0000000000000xl::;;;;;,'''''''',;;;;;::lk0000000000000d
 .d00000000000000000OkxxxdoooooooodxxxkO00000000000000000d.
   .;lxO00000000000000000000000000000000000000000000Oxl;.
        ..,;cloxkOO0000000000000000000000OOkxdlc;,..
                     ..................

"Oh, you may not think I'm pretty,
But don't judge on what you see,"

"For I'm the [Galaxy] Sorting Hat
And I can cap them all."

You might belong in Condor,
Where dwell the slow to compute,

You might belong in Pulsar,
Far flung and remote,

Or yet in wise old Singularity,
If you're evil and insecure

--hexylena
"""
import os
import yaml

from copy import deepcopy
from galaxy.jobs import JobDestination
from galaxy.jobs.mapper import JobMappingException
from random import sample
import math


class DetailsFromYamlFile:
    """
    Retrieve details from a yaml file
    """
    def __init__(self, yaml_file):
        yaml_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), yaml_file)
        if os.path.isfile(yaml_file_path):
            with open(yaml_file_path, 'r') as handle:
                self._conf = yaml.load(handle, Loader=yaml.SafeLoader)

    @property
    def conf(self):
        return self._conf

    def get(self, first_level_label, second_level_label=None):
        for key, value in self._conf.items():
            if key == first_level_label:
                if second_level_label is None:
                    return value
                else:
                    return value.get(second_level_label)
        return None

    def get_path(self, label):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.get('file_paths', label))


# Sorting Hat configuration details are defined in this file
SH_CONFIGURATION_FILENAME = 'sorting_hat.yaml'

sh_conf = DetailsFromYamlFile(SH_CONFIGURATION_FILENAME)
DEFAULT_DESTINATION = sh_conf.get('default_destination')
DEFAULT_TOOL_SPEC = sh_conf.get('default_tool_specification')
FAST_TURNAROUND = sh_conf.get('fast_turnaround')
FDID_PREFIX = sh_conf.get('force_destination_id_prefix')
SPECIAL_TOOLS = sh_conf.get('special_tools')

# The default / base specification for the different environments.
SPECIFICATION_PATH = sh_conf.get_path('destination_specifications')
SPECIFICATIONS = DetailsFromYamlFile(SPECIFICATION_PATH).conf

TOOL_DESTINATION_PATH = sh_conf.get_path('tool_destinations')
TOOL_DESTINATIONS = DetailsFromYamlFile(TOOL_DESTINATION_PATH).conf

JOINT_DESTINATIONS_PATH = sh_conf.get_path('joint_destinations')
JOINT_DESTINATIONS = DetailsFromYamlFile(JOINT_DESTINATIONS_PATH).conf


def assert_permissions(tool_spec, user_email, user_roles):
    """
    Permissions testing.

    - default state is to allow everyone to run everything.
    - If there is a permissions block, `deny: all` is the default.
    - We ONLY support allowing specific users to run something. This DOES NOT
      support preventing specific users from running something.

    """
    exception_text = "This tool is temporarily disabled due to internal policy. Please contact us if you have issues."
    # If there is no permissions block then it's going to be fine for everyone.
    if 'permissions' not in tool_spec:
        return

    permissions = tool_spec['permissions']

    # TODO(hxr): write a custom tool thing linter.
    # We'll be extra defensive here since I don't think I trust us to get
    # linting right for now.
    if len(permissions.keys()) == 0:
        raise Exception("JCaaS Configuration error 1")

    # And for typos.
    if 'allow' not in permissions:
        raise Exception("JCaaS Configuration error 2")

    if 'users' not in permissions['allow'] and 'roles' not in permissions['allow']:
        raise Exception("JCaaS Configuration error 3")
    # ENDTODO

    # Pull out allowed users and roles, defaulting to empty lists if the keys
    # aren't there.
    allowed_users = permissions['allow'].get('users', [])
    allowed_roles = permissions['allow'].get('roles', [])

    # If the user is on our list, yay, return.
    if user_email in allowed_users:
        return

    # If one of their roles is in our list
    if any([user_role in allowed_roles for user_role in user_roles]):
        return

    # Auth failure.
    raise Exception(exception_text)


def change_object_store_dependent_on_user(params, user_roles):
    """
    Different roles can have their own storage. Here we overwrite the object store based on user associated roles.
    Example: A user belongs to the role 'dataplant'. Those users own dedicated storage that they include into Galaxy.
        Here, we change the 'object_store_id' based in the role 'dataplant'.
    """
    if 'dataplant' in user_roles:
        params['object_store_id'] = 'dataplant01'
    # test new storage engines
    if 'storage-test' in user_roles:
        params['object_store_id'] = 's3_netapp01'
    return params


def get_tool_id(tool_id):
    """
    Convert ``toolshed.g2.bx.psu.edu/repos/devteam/column_maker/Add_a_column1/1.1.0``
    to ``Add_a_column``

    :param str tool_id: a tool id, can be the short kind (e.g. upload1) or the long kind with the full TS path.

    :returns: a short tool ID.
    :rtype: str
    """
    if tool_id.count('/') == 0:
        # E.g. upload1, etc.
        return tool_id

    # what about odd ones.
    if tool_id.count('/') == 5:
        (server, _, owner, repo, name, version) = tool_id.split('/')
        return name

    return tool_id


def name_it(tool_spec, prefix=FDID_PREFIX):
    """
    Create a destination's name using the tool's specification.
    Can be also forced to return a specific string
    """
    if 'cores' in tool_spec:
        name = '%scores_%sG' % (tool_spec.get('cores', 1), tool_spec.get('mem', 4))
    elif len(tool_spec.keys()) == 0 or (len(tool_spec.keys()) == 1 and 'runner' in tool_spec):
        name = '%s_default' % tool_spec.get('runner')
    else:
        name = '%sG_memory' % tool_spec.get('mem', 4)

    if tool_spec.get('tmp', None) == 'large':
        name += '_large'

    if 'name' in tool_spec:
        name += '_' + tool_spec['name']

    # Force a replacement of the destination's id
    if tool_spec.get('force_destination_id', False):
        name = prefix + tool_spec.get('runner')

    return name


def _get_limits(destination, dest_spec=SPECIFICATIONS, default_cores=1, default_mem=4, default_gpus=0):
    """
    Get destination's limits
    """
    limits = {'cores': default_cores, 'mem': default_mem, 'gpus': default_gpus}
    limits.update(dest_spec.get(destination).get('limits', {}))
    return limits


def _weighted_random_sampling(destinations, dest_spec):
    bunch = []
    for d in destinations:
        weight = dest_spec[d].get('nodes', 1)
        bunch += [d] * weight
    destination = sample(bunch, 1)[0]
    return destination


def build_spec(tool_spec, dest_spec, runner_hint=None):
    destination = runner_hint if runner_hint else tool_spec.get('runner')

    if destination not in dest_spec:
        if destination in JOINT_DESTINATIONS:
            destination = _weighted_random_sampling(JOINT_DESTINATIONS[destination], dest_spec)
        else:
            destination = DEFAULT_DESTINATION

    env = dict(dest_spec.get(destination, {'env': {}})['env'])
    params = dict(dest_spec.get(destination, {'params': {}})['params'])
    tags = {dest_spec.get(destination).get('tags', None)}

    # We define the default memory and cores for all jobs.
    tool_memory = tool_spec.get('mem')
    tool_cores = tool_spec.get('cores')
    tool_gpus = tool_spec.get('gpus')

    # We apply some constraints to these values, to ensure that we do not
    # produce unschedulable jobs, requesting more ram/cpu than is available in a
    # given location. Currently we clamp those values rather than intelligently
    # re-scheduling to a different location due to TaaS constraints.
    limits = _get_limits(destination, dest_spec=dest_spec)
    tool_memory = min(tool_memory, limits.get('mem'))
    tool_cores = min(tool_cores, limits.get('cores'))
    tool_gpus = min(tool_gpus, limits.get('gpus'))

    kwargs = {
        # Higher numbers are lower priority, like `nice`.
        'PRIORITY': tool_spec.get('priority', 128),
        'MEMORY': str(tool_memory) + 'G',
        'MEMORY_MB': int(tool_memory * 1024),
        'PARALLELISATION': tool_cores,
        'NATIVE_SPEC_EXTRA': "",
        'GPUS': tool_gpus,
    }

    if 'docker_enabled' in params and params['docker_enabled']:
        for k in tool_spec:
            if k.startswith('docker'):
                params[k] = tool_spec.get(k, '')

    if 'remote_cluster_mq' in destination:
        # specific for remote condor cluster
        if tool_gpus == 0 and 'submit_request_gpus' in params:
            del params['submit_request_gpus']

    # Update env and params from kwargs.
    env.update(tool_spec.get('env', {}))
    env = {k: str(v).format(**kwargs) for (k, v) in env.items()}

    params.update(tool_spec.get('params', {}))
    for (k, v) in params.items():
        if not isinstance(v, list):
            params[k] = str(v).format(**kwargs)
        else:
            params[k] = v

    tags.add(tool_spec.get('tags', None))
    tags.discard(None)
    tags = ','.join([x for x in tags if x is not None]) if len(tags) > 0 else None

    if 'condor' in destination:
        runner = 'condor'
    elif 'slurm' in destination:
        runner = 'slurm'
    elif 'pulsar_embedded' in destination:
        runner = 'pulsar_embedded'
    elif 'remote_cluster_mq' in destination:
        # destination label has to follow this convention:
        # remote_cluster_mq_feature1_feature2_feature3_pulsarid
        runner = "_".join(['pulsar_eu', destination.split('_').pop()])
    else:
        runner = 'local'

    env = [dict(name=k, value=v) for (k, v) in env.items()]
    return env, params, runner, tags


def reroute_to_dedicated(user_roles):
    """
    Re-route users to correct destinations. Some users will be part of a role
    with dedicated training resources.
    """
    # Collect their possible training roles identifiers.
    training_roles = [role for role in user_roles if role.startswith('training-')]

    # Some particular events can have contemporary trainings (like GCC) and we want to collect
    # them under the same label (e.g. to assign the the same computing cluster)
    if any([role.startswith('training-gcc-') for role in training_roles]):
        training_roles.append('training-gcc')

    if len(training_roles) > 0:
        # The user does have one or more training roles.
        # So we must construct a requirement / ranking expression.
        training_expr = " || ".join(['(GalaxyGroup == "%s")' % role for role in training_roles])
        training_labels = '"' + ", ".join(['%s' % role for role in training_roles]) + '"'
        return {
            # We require that it does not run on machines that the user is not in the role for.
            # We then rank based on what they *do* have the roles for.
            'params': {
                'requirements': '(GalaxyGroup == "compute") || (%s)' % training_expr,
                '+Group': training_labels,
            }
        }
    return {}


def _finalize_tool_spec(tool_id, tools_spec, user_roles, memory_scale=1.0):
    # Find the 'short' tool ID which is what is used in the .yaml file.
    tool = get_tool_id(tool_id)
    # Pull the tool specification (i.e. job destination configuration for this tool)
    tool_spec = deepcopy(tools_spec.get(tool, {}))
    # Update the tool specification with any training resources that are available
    tool_spec.update(reroute_to_dedicated(user_roles))

    # Update the tool specification with default values if they are not present
    for s in DEFAULT_TOOL_SPEC:
        tool_spec[s] = tool_spec.get(s, DEFAULT_TOOL_SPEC[s])

    tool_spec['mem'] *= memory_scale

    return tool_spec


def _gateway(tool_id, user_preferences, user_roles, user_id, user_email,
             ft=FAST_TURNAROUND, special_tools=SPECIAL_TOOLS,
             tools_spec=TOOL_DESTINATIONS, dest_spec=SPECIFICATIONS,
             memory_scale=1.0):
    tool_spec = _finalize_tool_spec(tool_id, tools_spec, user_roles, memory_scale=memory_scale)

    # Now build the full spec

    # Use this hint to force a destination (e.g. defined from the user's preferences)
    # but not for all tools
    runner_hint = None
    tools_to_skip = [k for k, v in special_tools.items() if 'skip_user_preferences' in v]
    if tool_id not in tools_to_skip:
        for data_item in user_preferences:
            if "distributed_compute|remote_resources" in data_item:
                if user_preferences[data_item] != "None":
                    runner_hint = user_preferences[data_item]

    # If a tool is in the pulsar_incompatible list, force the default destination.
    tools_pulsar_incompatible = [k for k, v in special_tools.items() if 'pulsar_incompatible' in v]
    # print(tool_spec['runner'], tool_id, dest_spec.get(tool_spec['runner']).get('info'))
    if tool_id in tools_pulsar_incompatible and dest_spec.get(tool_spec['runner']).get('info').get('remote'):
        runner_hint = DEFAULT_DESTINATION

    # Ensure that this tool is permitted to run, otherwise, throw an exception.
    assert_permissions(tool_spec, user_email, user_roles)

    env, params, runner, tags = build_spec(tool_spec, dest_spec, runner_hint=runner_hint)
    params['accounting_group_user'] = str(user_id)
    params['description'] = get_tool_id(tool_id)

    # This is a special case, we're requiring it for faster feedback / turnaround times.
    # Fast turnaround can be enabled for all the jobs or per single user adding a user role
    # with the label described by 'role_label' key.
    ft_enabled = ft.get('enabled')
    ft_mode = ft.get('mode')
    ft_role_label = ft.get('role_label')
    ft_requirements = ft.get('requirements')

    if ft_enabled:
        if (ft_mode == 'user_roles' and ft_role_label in user_roles) or ft_mode == 'all_jobs':
            params['requirements'] = ft_requirements

    return env, params, runner, tool_spec, tags


def _special_case(param_dict, tool_id, user_id, user_roles):
    """"
    Tools to block before starting to run
    """
    if get_tool_id(tool_id).startswith('interactive_tool_') and user_id == -1:
        raise JobMappingException("This tool is restricted to registered users, "
                                  "please contact a site administrator")

    if get_tool_id(tool_id).startswith('interactive_tool_ml') and 'interactive-tool-ml-jupyter-notebook' not in user_roles:
        raise JobMappingException("This tool is restricted to authorized users, "
                                  "please contact a site administrator")

    if get_tool_id(tool_id).startswith('gmx_sim'):
        md_steps_limit = 1000000
        if 'md_steps' in param_dict['sets']['mdp']:
            if param_dict['sets']['mdp']['md_steps'] > md_steps_limit and 'gmx_sim_powerusers' not in user_roles:
                raise JobMappingException("this tool's configuration has exceeded a computational limit, "
                                          "please contact a site administrator")

    return


def gateway(tool_id, user, memory_scale=1.0, next_dest=None):
    if user:
        user_roles = [role.name for role in user.all_roles() if not role.deleted]
        user_preferences = user.extra_preferences
        email = user.email
        user_id = user.id
    else:
        user_roles = []
        user_preferences = []
        email = ''
        user_id = -1

    try:
        env, params, runner, spec, tags = _gateway(tool_id, user_preferences, user_roles, user_id, email,
                                                   ft=FAST_TURNAROUND, special_tools=SPECIAL_TOOLS,
                                                   memory_scale=memory_scale)
    except Exception as e:
        return JobMappingException(str(e))

    resubmit = []
    if next_dest:
        resubmit = [{
            'condition': 'any_failure and attempt <= 3',
            'destination': next_dest
        }]

    name = name_it(spec)
    params = change_object_store_dependent_on_user(params, user_roles)
    return JobDestination(
        id=name,
        tags=tags,
        runner=runner,
        params=params,
        env=env,
        resubmit=resubmit,
    )


def gateway_1x(tool_id, user):
    return gateway(tool_id, user, memory_scale=1, next_dest='gateway_1_5x')


def gateway_1_5x(tool_id, user):
    return gateway(tool_id, user, memory_scale=1.5, next_dest='gateway_2x')


def gateway_2x(tool_id, user):
    return gateway(tool_id, user, memory_scale=2)


def gateway_checkpoint(app, job, tool, user):
    """"
    These are tools that have to be blocked before starting to run, if a particular condition arise.
    If not, reroute to gateway single run.
    """
    param_dict = dict([(p.name, p.value) for p in job.parameters])
    param_dict = tool.params_from_strings(param_dict, app)
    tool_id = tool.id
    if user:
        user_roles = [role.name for role in user.all_roles() if not role.deleted]
        user_id = user.id
    else:
        user_roles = []
        user_id = -1

    _special_case(param_dict, tool_id, user_id, user_roles)

    return gateway(tool_id, user)


def _compute_memory_for_hifiasm(param_dict):
    computed_memory = 0
    converter = {
        'g': 1,
        'G': 1,
        'm': 1000,
        'M': 1000,
        'k': 1000000,
        'K': 1000000
    }
    kcov = 36
    if 'advanced_options' in param_dict:
        if 'kcov' in param_dict['advanced_options']:
            kcov = param_dict['advanced_options']['kcov']
        if 'hg_size' in param_dict['advanced_options']:
            hg_size = param_dict['advanced_options']['hg_size']
            if len(hg_size) > 1:
                hg_size_suffix = hg_size[-1:]
                hg_size_value = float(hg_size[:len(hg_size)-1].replace(",", "."))
                # (len*(kmercov*2) * 1.75
                hg_size_value_in_Gb = hg_size_value / converter[hg_size_suffix]
                computed_memory = math.ceil(hg_size_value_in_Gb*(kcov*2)*1.75)

    return computed_memory


def gateway_for_hifiasm(app, job, tool, user, next_dest=None):
    """"
    The memory requirement of Hifiasm depends on a wrapper's input
    """
    param_dict = dict([(p.name, p.value) for p in job.parameters])
    param_dict = tool.params_from_strings(param_dict, app)
    tool_id = tool.id
    if user:
        user_roles = [role.name for role in user.all_roles() if not role.deleted]
        user_preferences = user.extra_preferences
        email = user.email
        user_id = user.id
    else:
        user_roles = []
        user_preferences = []
        email = ''
        user_id = -1

    try:
        env, params, runner, spec, tags = _gateway(tool_id, user_preferences, user_roles, user_id, email,
                                                   ft=FAST_TURNAROUND, special_tools=SPECIAL_TOOLS)
    except Exception as e:
        return JobMappingException(str(e))

    limits = _get_limits(runner)
    request_memory = min(max(_compute_memory_for_hifiasm(param_dict), spec['mem']), limits.get('mem'))
    params['request_memory'] = "{}{}".format(request_memory, 'G')

    resubmit = []
    if next_dest:
        resubmit = [{
            'condition': 'any_failure and attempt <= 3',
            'destination': next_dest
        }]

    spec['mem'] = request_memory
    name = name_it(spec)
    return JobDestination(
        id=name,
        tags=tags,
        runner=runner,
        params=params,
        env=env,
        resubmit=resubmit,
    )
