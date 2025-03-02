#!/bin/bash
cd cash_register
apt-get update
apt-get install -y wkhtmltopdf
python3 manage.py migrate
python3 manage.py test
python3 manage.py loaddata item_fixture.json
python3 manage.py runserver 0.0.0.0:8000