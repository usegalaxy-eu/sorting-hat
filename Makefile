# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(VENV)/bin

help:
	@echo "Please digit \`make _target_\` "
	@echo " "
	@echo "  lint"
	@echo "  clean              to make some cleans"
	@echo "  test               to run tests"
	@echo "  test-eu            to run tests using Usegalaxy.eu details"

.PHONY: test lint clean $(VENV)

test: galaxy/jobs $(VENV)
	. venv/bin/activate ; \
	$(PY) -m unittest discover -s tests

test-eu: galaxy/jobs $(VENV)
	wget https://raw.githubusercontent.com/usegalaxy-eu/infrastructure-playbook/master/files/galaxy/dynamic_rules/usegalaxy/destination_specifications.yaml -O destination_specifications.yaml
	wget https://raw.githubusercontent.com/usegalaxy-eu/infrastructure-playbook/master/files/galaxy/dynamic_rules/usegalaxy/tool_destinations.yaml -O tool_destinations.yaml
	. $(BIN)/activate ; \
	$(PY) -m unittest discover -s tests
	git checkout -- destination_specifications.yaml
	git checkout -- tool_destinations.yaml

lint: $(VENV)
	$(BIN)/flake8 --exclude $(VENV) --count --select=E9,F63,F7,F82 --show-source --statistics
	$(BIN)/flake8 --exclude $(VENV) --count --exit-zero --ignore=E501 --statistics

clean:
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf galaxy $(VENV)

galaxy/jobs:
	mkdir -p galaxy/jobs
	echo "class JobDestination:" > galaxy/jobs/__init__.py
	echo '    """"""' >> galaxy/jobs/__init__.py
	echo "class JobMappingException:" > galaxy/jobs/mapper.py
	echo '    """"""' >> galaxy/jobs/mapper.py

$(VENV): $(BIN)/activate

$(BIN)/activate: requirements.txt
	test -f $(BIN)/activate || $(PY) -m venv $(VENV)
	. $(BIN)/activate ;\
	$(BIN)/pip install -Ur requirements.txt
	touch venv/bin/activate
