web: gunicorn app:davesbread
init: python db_create.python
upgrade: db_upgrade.py