import os
import math

from . import Destination


class Sge(Destination):
    MAX_CORES = 24
    MAX_MEM = 256 - 2

    @classmethod
    def custom_spec(cls, tool_spec, params, kwargs, tool_memory, tool_cores):
        raw_allocation_details = {}

        if 'cores' in tool_spec:
            kwargs['PARALLELISATION'] = '-pe "pe*" %s' % tool_cores
            # memory is defined per-core, and the input number is in gigabytes.
            real_memory = int(1024 * tool_memory / tool_spec['cores'])
            # Supply to kwargs with M for megabyte.
            kwargs['MEMORY'] = '%sM' % real_memory
            raw_allocation_details['mem'] = tool_memory
            raw_allocation_details['cpu'] = tool_cores

        if 'nativeSpecExtra' in tool_spec:
            kwargs['NATIVE_SPEC_EXTRA'] = tool_spec['nativeSpecExtra']

        # Large TMP dir
        if tool_spec.get('tmp', None) == 'large':
            kwargs['NATIVE_SPEC_EXTRA'] += '-l has_largetmp=1'

        # Environment variables, SGE specific.
        if 'env' in tool_spec and '_JAVA_OPTIONS' in tool_spec['env']:
            params['nativeSpecification'] = params['nativeSpecification'].replace('-v _JAVA_OPTIONS', '')
        return kwargs, raw_allocation_details, params

    @classmethod
    def is_available(cls):
        try:
            os.stat('/usr/local/galaxy/temporarily-disable-drmaa')
            return False
        except OSError:
            return True

    @classmethod
    def reroute_to_dedicated(cls, tool_spec, user_roles):
        return {}

    @classmethod
    def convert(cls, tool_spec):
        # Send this to SGE
        tool_spec['runner'] = 'sge'
        # SGE does not support partials
        tool_spec['mem'] = int(math.ceil(tool_spec['mem']))
        return tool_spec
