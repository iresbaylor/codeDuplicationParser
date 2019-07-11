#!/bin/bash

# Script to check the sources for all detectable errors and issues

./check-bashscripts.sh
./check-docstyle.sh
./detect-common-errors.sh
./detect-dead-code.sh
./run-linter.sh
