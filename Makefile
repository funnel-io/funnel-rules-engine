PYTHON_VERSION ?= 3.8

dist: clean-dist
	python3 setup.py sdist

setup: venv

venv: dev-packages.txt
	virtualenv venv --python=${PYTHON_VERSION}
	. venv/bin/activate; pip3 install \
	-r dev-packages.txt

.PHONY: test
test: venv
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -rsx --flake8 tests/ src/ --cov ./src/rules_engine/ --no-cov-on-fail --cov-report term-missing --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8  src --exclude '#*,~*,.#*'

.PHONY: clean
clean: clean-dist
	rm -rf venv

.PHONY: clean-dist
clean-dist:
	rm -rf build
	rm -rf src/funnel_rules_engine.egg-info
	rm -rf dist
