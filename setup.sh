#!/bin/bash

sudo apt-get install python3 python3-pip python3-virtualenv -y
mkdir venv
virtualenv venv/ceroxbot --python=python3
source venv/ceroxbot/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
