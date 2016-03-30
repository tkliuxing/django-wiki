.PHONY: help clean clean-pyc clean-build list test test-all coverage docs release sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	pep8 wiki

test:
	./runtests.py

test-all:
	tox

coverage:
	coverage run --source wiki setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	sphinx-build -b linkcheck ./docs _build/
	sphinx-build -b html ./docs _build/

release: clean assets
	echo "Creating HISTORY.rst..."
	echo "Latest Changes" > HISTORY.rst
	echo "==============" >> HISTORY.rst
	echo "" >> HISTORY.rst
	echo "This file is auto-generated upon every new release."
	echo "" >> HISTORY.rst
	echo "Compiled on: `date`::" >> HISTORY.rst
	echo "" >> HISTORY.rst
	git log --graph --pretty=format:'%h -%d %s (%cr) <%an>' --abbrev-commit | sed "s/^/    /" >> HISTORY.rst
	echo "Packing source dist..."
	python3 setup.py sdist bdist_wheel upload --sign
	# twine upload -s dist/*

assets:
	lessc wiki/static/wiki/bootstrap/less/wiki/wiki-bootstrap.less wiki/static/wiki/bootstrap/css/wiki-bootstrap.css
	lessc -x wiki/static/wiki/bootstrap/less/wiki/wiki-bootstrap.less wiki/static/wiki/bootstrap/css/wiki-bootstrap.min.css

sdist: clean assets
	python setup.py sdist
	ls -l dist
