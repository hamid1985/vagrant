#!/bin/bash
sudo apt-get update
sudo ln -s /usr/bin/python3 /usr/bin/python
sudo apt-get install -y python3-pip
sudo ln -s /usr/bin/pip3 /usr/bin/pip
pip install --upgrade pip
sudo pip install troposphere awscli boto3 ansible
