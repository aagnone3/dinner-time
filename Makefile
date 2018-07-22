all := help package_prep package_test package run
.PHONY := all
.DEFAULT_GOAL := help
PYPI_TEST_URL ?= "https://test.pypi.org/legacy/"

help:
	@echo "General python application maintenance."
	@echo ""
	@echo "Targets:"
	@echo "  help           Print this help message."
	@echo "  test           Run tests in a Docker container (not yet supported)."
	@echo "  package        Package the current code and upload to the official PyPi server."
	@echo "  package_test   Package the current code and upload to the test PyPi server."

package_prep:
	# remove previous packages (or make the directory
	[[ -d dist ]] && rm -rf dist/* || mkdir dist
	# generate the package
	pip install --upgrade twine
	python setup.py bdist_wheel

package_test: package_prep
	# upload the generated packages to the test PyPi server
	twine upload --repository-url ${PYPI_TEST_URL} dist/*

package: package_prep
	# upload the generated packages to the official PyPi server
	twine upload dist/*
