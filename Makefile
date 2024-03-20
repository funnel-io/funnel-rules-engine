PYTHON_VERSION ?= 3.9

dist: clean-dist setup
	. venv/bin/activate && python3 -m build .

.PHONY: setup
setup: venv/setup.txt

venv:
	virtualenv venv --python=${PYTHON_VERSION}

venv/setup.txt: venv dev-requirements.txt
	. venv/bin/activate && \
	pip3 install --upgrade pip && \
	pip3 install --requirement dev-requirements.txt
	touch venv/setup.txt

.PHONY: test
test: setup
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -rsx tests/ src/ --cov ./src/rules_engine/ --no-cov-on-fail --cov-report term-missing --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8 src --exclude '#*,~*,.#*'
	@ . venv/bin/activate && black --check src tests
	@ . venv/bin/activate && mypy src

.PHONY: clean
clean: clean-dist
	rm -rf venv

.PHONY: clean-dist
clean-dist:
	rm -rf build
	rm -rf src/funnel_rules_engine.egg-info
	rm -rf dist

.PHONY: release
release: test dist
	. venv/bin/activate && twine upload dist/*

.PHONY: test-release
test-release: test dist
	. venv/bin/activate && twine upload -r testpypi dist/*
