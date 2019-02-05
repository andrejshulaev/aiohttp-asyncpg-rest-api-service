.DEFAULT_GOAL := help

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3.6


help:           ## Show available options with this Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


.PHONY: clean
clean:          ## Clean the docker-container, venv etc.
clean:
	docker-compose down -v
	docker rmi postgres:11-alpine
	rm -rf venv
	find -iname "*.pyc" -delete


venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3.6 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install docker-compose
	${PYTHON} -m pip install -e .
	touch $(VENV_NAME)/bin/activate


.PHONY: install_dep
install_dep:    ## Setup venv and install the application.
install_dep:
	make venv
	docker-compose up -d


.PHONY: run
run:            ## Run the application
run:
	${PYTHON} app