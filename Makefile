help:
	@echo "Please digit \`make _target_\` "
	@echo " "
	@echo "  clean              to make some cleans"
	@echo "  test               to run tests"

test: create_fake_galaxy_jobs_module venv
	. venv/bin/activate ; \
	python -m unittest discover -s tests

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

