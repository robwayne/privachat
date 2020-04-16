#!/bin/bash

export FLASK_APP=server/__init__.py
export FLASK_ENV=development
env FLASK_APP=server/__init__.py python3 -m initDatabaseCLI
flask init

open "http://localhost:5000"
