SHELL = bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# -----------------------------------------------------------------------------
# Section: Python

VENV = source venv/bin/activate &&
PY = ${VENV} python3

venv: pyproject.toml ## establish a virtual environment for python
	python3 -m venv venv && \
	${PY} -m pip install --upgrade pip
	${PY} -m pip install pytest	
	touch venv pyproject.toml


.PHONY: install 
install: .installed
.installed: venv pyproject.toml
	${PY} -m pip install -e .
	touch .installed	


.PHONY: test 
test: venv install
	${PY} -m pytest -s

.PHONY: clean-python
clean-python: 
	py3clean .

.PHONY: clean-venv
clean-venv: 
	rm -rf venv


.PHONY: clean-all
clean-all: clean-python clean-venv
	rm .installed
