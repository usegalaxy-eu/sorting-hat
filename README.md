# Job Configuration as a Service




```
$ JCAAS_CONF=config/main.yml python flask_job_conf.py &
$ curl -X POST -d '{"email": "hxr@local.host", "tool_id": "upload1", "user_roles": []}' -H 'Content-type: application/json' localhost:5000 --silent | jq
{
  "env": [
    {
      "name": "TEMP",
      "value": "/data/1/galaxy_db/tmp/"
    }
  ],
  "params": {
    "requirements": ""
  },
  "runner": "condor",
  "spec": {
    "env": {
      "TEMP": "/data/1/galaxy_db/tmp/"
    },
    "mem": 0.3,
    "requirements": "",
    "runner": "condor"
  }
}
```
