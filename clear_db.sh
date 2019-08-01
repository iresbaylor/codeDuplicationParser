#!/bin/bash

set -e

psql -f web/prepare_tables.pgsql cyclone
rm -rf engine/repos/
