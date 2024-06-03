#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = rep_1
PYTHON_VERSION = 3.12.3
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies
.PHONY: requirements
requirements:
	pipenv install
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 mod_1
	isort --check --diff --profile black mod_1
	black --check --config pyproject.toml mod_1

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml mod_1


## Download Data from storage system
.PHONY: sync_data_down
sync_data_down:
	aws s3 sync s3://ceie_proj_1/data/\
		data/ 
	

## Upload Data to storage system
.PHONY: sync_data_up
sync_data_up:
	aws s3 sync s3://ceie_proj_1/data/ data/\
		 --profile $(PROFILE)
	



## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	pipenv --python $(PYTHON_VERSION)
	@echo ">>> New pipenv created. Activate with:\npipenv shell"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make Dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) mod_1/data/make_dataset.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
