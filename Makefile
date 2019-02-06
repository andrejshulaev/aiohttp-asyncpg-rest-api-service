.DEFAULT_GOAL := help

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3.6


help:           ## Show available options with this Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


.PHONY: clean_all
clean_all:      ## Clean the docker-container, venv etc.
clean_all:
	docker-compose down -v
	docker rmi postgres:11-alpine &
	@rm -rf .Python MANIFEST build dist venv* *.egg-info *.egg*
	@find . -type f -name "*.py[co]" -exec rm -rv {} +
	@find . -type d -name "__pycache__" -exec rm -rv {} +


.PHONY: clean_venv
clean_venv:     ## Clean the venv.
clean_venv:
	@rm -rf .Python MANIFEST build dist venv* *.egg-info *.egg*
	@find . -type f -name "*.py[co]" -exec rm -rv {} +
	@find . -type d -name "__pycache__" -exec rm -rv {} +



.PHONY : test
test:           ## Run all the tests
test:
	${PYTHON} setup.py test


venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3.6 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install docker-compose
	${PYTHON} -m pip install gunicorn
	${PYTHON} -m pip install -e .
	touch $(VENV_NAME)/bin/activate


.PHONY: install_dep
install_dep:    ## Setup venv and install the application.
install_dep:
	make venv
	docker-compose up -d


.PHONY: run
run:            ## Run the application with simple aiohttp server
run:
	${PYTHON} app -



.PHONY : dev_run
dev_run:        ## Run application in a dev mode, where gunicorn workers will reload the application on every change.
dev_run:
	make install_dep
	exec venv/bin/gunicorn 'app.server:APP' --env config_file=`pwd`/config/config.yaml --bind localhost:8000 --worker-class aiohttp.GunicornWebWorker --reload \
		--log-level=debug --log-file=-
