TOP_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

rshell:	init
	source ${TOP_DIR}/.venv/bin/activate; \
	${TOP_DIR}/.venv/bin/rshell

init:
	if [ ! -d "${TOP_DIR}/.venv/" ]; then \
		python3 -m virtualenv ${TOP_DIR}/.venv/; \
		source ${TOP_DIR}/.venv/bin/activate; \
		pip3 install rshell; \
	fi
