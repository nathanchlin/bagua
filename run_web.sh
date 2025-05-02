#!/bin/bash
cd iching/src
export FLASK_APP=app.py
python3 -m flask run --port 5005 