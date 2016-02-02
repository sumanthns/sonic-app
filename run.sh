#!/bin/bash

export DATABASE_URL="mysql://root@localhost/sonic_app"

python sonic_app/manage.py runserver