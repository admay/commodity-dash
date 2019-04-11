.PHONY: default install lint test run-dev run-prod
.DEFAULT_GOAL := default

help:
	echo "Commands are 'sys-check', 'install', 'lint', 'test', 'run-prod', and 'run-dev'"

install:
	pip3 install -r requirements.txt

lint:
	flake8 *.py

test:
	pytest --verbose --color=yes

run-dev:
	python3 app.py -d true

run-prod:
	python3 app.py -d false

default: install lint test run-dev
