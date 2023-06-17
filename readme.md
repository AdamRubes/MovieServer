python -m venv venv

venv/scripts/activate.ps1

pip install -r requirements.txt

py manage.py makemigrations

py manage.py migrate

py manage.py loaddata fixtures/*

py manage.py makemigrations

py manage.py migrate