TOP_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

rshell:	init
	echo "Starting rshell; connect with 'connect serial /dev/ttyACM0 115200'..."
	source ${TOP_DIR}/.venv/bin/activate; \
	${TOP_DIR}/.venv/bin/rshell

screen:
	echo "Entering screen session: Press control-c when receiving sensor data stream, Exit with Ctrl-a k"
	screen /dev/ttyACM0 115200

init:
	if [ ! -d "${TOP_DIR}/.venv/" ]; then \
		python3 -m virtualenv ${TOP_DIR}/.venv/; \
		source ${TOP_DIR}/.venv/bin/activate; \
		pip3 install rshell; \
	fi
