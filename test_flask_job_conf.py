import sys


def _compare_val(expected, observed):
    assert expected == observed, '\n\tObserved: %s\n\tExpected: %s\n' % (observed, expected)


def _compare(expected, observed):
    assert len(observed.keys()) == len(expected.keys()), 'o:%s != e:%s' % (','.join(observed.keys()), ','.join(expected.keys()))
    for k in expected.keys():
        assert expected[k] == observed[k], '\n\tObserved: %s\n\tExpected: %s\n' % (observed, expected)


class subprocess(object):
    machines1 = """
Machine = "vgcnbwc-01.novalocal"

Machine = "vgcnbwc-02.novalocal"

Machine = "vgcnbwc-03.novalocal"

Machine = "vgcnbwc-training-gcc-01.novalocal"

Machine = "vgcnbwc-training-gcc-02.novalocal"

Machine = "vgcnbwc-training-asdf-01.novalocal"

Machine = "vgcnbwc-upload-01.novalocal"

Machine = "vgcnbwc-metadata-01.novalocal"

Machine = "unrelated-01.novalocal"

Machine = "unrelated-02.novalocal"
    """

    machines2 = """
Machine = "vgcnbwc-01.novalocal"

Machine = "vgcnbwc-02.novalocal"

Machine = "vgcnbwc-03.novalocal"

Machine = "vgcnbwc-training-gcc-04.novalocal"

Machine = "vgcnbwc-training-gcc-03.novalocal"

Machine = "vgcnbwc-training-asdf-01.novalocal"

Machine = "vgcnbwc-training-asdf-02.novalocal"

Machine = "vgcnbwc-upload-01.novalocal"

Machine = "vgcnbwc-metadata-01.novalocal"

Machine = "unrelated-01.novalocal"

Machine = "unrelated-02.novalocal"
    """

    current = machines2
    @classmethod
    def check_output(cls, *args, **kwargs):
        if not cls.condor_is_alive:
            raise cls.CalledProcessError()
        return cls.current

    @classmethod
    def reset(cls):
        cls.current = cls.machines1

    @classmethod
    def swap(cls):
        if cls.current == cls.machines1:
            cls.current = cls.machines2
        elif cls.current == cls.machines2:
            cls.current = cls.machines1


    condor_is_alive = False
    @classmethod
    def check_call(cls, *args, **kwargs):
        if not cls.condor_is_alive:
            raise cls.CalledProcessError()
        return

    @classmethod
    def condor_death_toggle(cls):
        cls.condor_is_alive = not cls.condor_is_alive

    class CalledProcessError(Exception):
        pass

    # python3
    PIPE = None
    STDOUT = None
    STDERR = None
    DEVNULL = None
    @classmethod
    def _args_from_interpreter_flags(cls, *args, **kwargs):
        return

sys.modules['subprocess'] = subprocess


import json
import unittest
import flask_job_conf


class FlaskJobConfTestCase(unittest.TestCase):

    def setUp(self):
        flask_job_conf.app.testing = True
        self.app = flask_job_conf.app.test_client()

    def test_no_params(self):
        rv = self.app.post('/')
        assert rv.data == b'{"error":"missing content or content-type header"}\n', rv.data

    def test_upload_spec_drmaa(self):
        sys.modules['subprocess'].condor_is_alive = False
        payload = {
            'tool_id': 'upload1',
            'user_roles': ['test'],
            'email': 'hxr@informatik.uni-freiburg.de',
        }
        rv = self.app.post('/', headers={'Content-type': 'application/json'}, data=json.dumps(payload))
        resp = json.loads(rv.data.decode())
        print(resp)
        _compare(resp['params'], {'nativeSpecification': '-q galaxy1.q,all.q -p -128 -l galaxy1_slots=1 -l h_vmem=4G   -v _JAVA_OPTIONS -v TEMP -v TMPDIR -v PATH -v PYTHONPATH -v LD_LIBRARY_PATH -v XAPPLRESDIR -v GDFONTPATH -v GNUPLOT_DEFAULT_GDFONT -v MPLCONFIGDIR -soft -l galaxy1_dedicated=1'})
        _compare_val(resp['runner'], 'drmaa')
        _compare(resp['spec'], {'mem': 4, 'runner': 'sge', 'env': {'TEMP': '/data/1/galaxy_db/tmp/'}, 'requirements': '( (machine == "vgcnbwc-upload-01.novalocal") )'})

    def test_upload_spec_condor(self):
        sys.modules['subprocess'].condor_is_alive = True

        payload = {
            'tool_id': 'upload1',
            'user_roles': ['test', 'v'],
            'email': 'hxr@informatik.uni-freiburg.de',
        }
        rv = self.app.post('/', headers={'Content-type': 'application/json'}, data=json.dumps(payload))
        resp = json.loads(rv.data.decode())
        _compare(resp['params'], {'request_memory': '0.3G', 'requirements': '( (machine == "vgcnbwc-upload-01.novalocal") )', 'priority': '-128'})
        _compare_val(resp['runner'], 'condor')
        _compare(resp['spec'], {'mem': 0.3, 'runner': 'condor', 'env': {'TEMP': '/data/1/galaxy_db/tmp/'}, 'requirements': '( (machine == "vgcnbwc-upload-01.novalocal") )'})


if __name__ == '__main__':
    unittest.main()
