# Netman - Mikrotik

IP Address Management And Mikrotik DHCP, DNS Management

## Requirement

Ubuntu / Debian 

Package **nmap** already installed 

Python 3.9.5

Django 3.2.4

## Installation

Edit ***host***, ***user*** and ***password*** in ***ddi/mikrotik.py*** according to your mikrotik

Migrate model to database

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Run Application

```bash
python3 manage.py runserver 0.0.0.0:8080
```