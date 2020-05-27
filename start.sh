#!/bin/bash

gunicorn --chdir api chess:api -w 10 -b 0.0.0.0:80
