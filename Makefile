#!/usr/bin/make
# WARN: gmake syntax
########################################################
# Makefile for Battleschool
#
# useful targets:
#   make sdist ---------------- produce a tarball

########################################################
# variable section

PYTHON=python

########################################################

all: clean python

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo "Cleaning up editor backup files"
	find . -type f \( -name "*~" -or -name "#*" \) -delete
	find . -type f \( -name "*.swp" \) -delete

python:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

sdist: clean
	$(PYTHON) setup.py sdist -t MANIFEST.in
