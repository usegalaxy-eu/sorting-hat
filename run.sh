#!/bin/bash
exec gunicorn --workers 1 --bind localhost:8090 flask_job_conf:app
