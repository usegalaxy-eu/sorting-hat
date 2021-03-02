help:
	@echo "Please digit \`make _target_\` "
	@echo " "
	@echo "  clean              to make some cleans"
	@echo "  test               to run tests"
	@echo "  test-eu            to run tests using Usegalaxy.eu details"

test: create_fake_galaxy_jobs_module venv
	. venv/bin/activate ; \
	python -m unittest discover -s tests

test-eu: create_fake_galaxy_jobs_module venv
	wget https://raw.githubusercontent.com/usegalaxy-eu/infrastructure-playbook/master/files/galaxy/dynamic_rules/usegalaxy/destination_specifications.yaml -O destination_specifications.yaml
	wget https://raw.githubusercontent.com/usegalaxy-eu/infrastructure-playbook/master/files/galaxy/dynamic_rules/usegalaxy/tool_destinations.yaml -O tool_destinations.yaml
	. venv/bin/activate ; \
	python -m unittest discover -s tests
	git checkout -- destination_specifications.yaml
	git checkout -- tool_destinations.yaml

clean:
	find . -name '*.pyc' -delete
	rm -rf galaxy venv
	find . -type d -name '__pycache__' -exec rm -rf {} +

create_fake_galaxy_jobs_module:
	mkdir -p galaxy/jobs
	echo "class JobDestination: " > galaxy/jobs/__init__.py
	echo '    """"""' >> galaxy/jobs/__init__.py
	echo "class JobMappingException:" > galaxy/jobs/mapper.py
	echo '    """"""' >> galaxy/jobs/mapper.py

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -f venv/bin/activate || virtualenv -p $(shell which python3) venv
	. venv/bin/activate ;\
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

