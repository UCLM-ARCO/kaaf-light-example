#!/usr/bin/make -f

WRAPPER_PID=.scone/scone-wrapper.pid
SCONE_PID=.scone/scone.pid

all: scone-start run-case-1

.ONESHELL:
scone-start:
	scone-wrapper &

scone-stop:
	kill -2 $$(cat ${WRAPPER_PID})

run-case-1:
	./gen-rules.py case-1.scene --Ice.Config=scone.config