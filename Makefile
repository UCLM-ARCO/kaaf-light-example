#!/usr/bin/make -f

WRAPPER_PID=.scone/scone-wrapper.pid
SCONE_PID=.scone/scone.pid

all: scone-start run-usecase

.ONESHELL:
scone-start:
	scone-wrapper & sleep 3

scone-stop:
	kill -2 $$(cat ${WRAPPER_PID})

run-usecase:
	./kaaf.py usecase.scenario --Ice.Config=scone.config
