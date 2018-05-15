#!/bin/bash
. {{ jobconf_venv }}/bin/activate
exec gunicorn --workers {{ jobconf_workers }} --bind {{ jobconf_bind }} flask_job_conf:app
