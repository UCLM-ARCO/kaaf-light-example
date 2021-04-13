#!/usr/bin/make -f
# -*- mode:makefile -*-

PROJECT_DIR := $(shell get-project-dir)

all: clean \
	run-scone \
	gen-rules

gen-rules:
	$(PROJECT_DIR)/gen-rules.py scene.json --Ice.Config=$(PROJECT_DIR)/gen-rules.config

run-scone:
	cd $(PROJECT_DIR); \
	gnome-terminal -x sh -c "scone-wrapper; bash"
	sleep 1

clean:
	cd $(PROJECT_DIR); \
	$(RM) -r .scone