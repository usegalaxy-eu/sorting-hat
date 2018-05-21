import os
import math

from . import Destination


class Local(Destination):
    MAX_CORES = 1
    MAX_MEM = 2

    @classmethod
    def custom_spec(cls, tool_spec, params, kwargs, tool_memory, tool_cores):
        raw_allocation_details = {}
        raw_allocation_details['mem'] = tool_memory
        raw_allocation_details['cpu'] = tool_cores

        return {}, raw_allocation_details, {}

    @classmethod
    def is_available(cls):
        try:
            os.stat('/usr/local/galaxy/temporarily-disable-local')
            return False
        except OSError:
            return True

    @classmethod
    def convert(cls, tool_spec):
        # Send this to SGE
        tool_spec['runner'] = 'local'
        return tool_spec
