#!/bin/sh
coverage run --source=zmqfirewall/ setup.py test
coverage report -m
