#!/bin/bash

set -e

psql -f web/prepare_tables.pgsql code_duplication
rm -rf engine/repos/
