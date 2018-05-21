debug:
	JCAAS_CONF=config/main.yml FLASK_ENV=development FLASK_APP=flask_job_conf flask run --reload

run:
	exec gunicorn --workers 4 --bind localhost:8090 flask_job_conf:app

query:
	curl \
		-X POST \
		-H 'Content-type: application/json' \
		-d '{"tool_id": "asdf", "user_roles": [], "email": "hxr@local.host"}' \
	localhost:5000
