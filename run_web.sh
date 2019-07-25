#!/bin/bash

set -e

export FLASK_ENV="development"
export FLASK_APP="web/app.py"

flask run
