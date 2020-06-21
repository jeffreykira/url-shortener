import logging
import logging.config
import os
import time
import subprocess
from url_shortener import logging_config
from flask import Flask, Blueprint, request, g
from shutil import which

log = logging.getLogger(__name__)
flask_app = Flask(__name__)

if which('docker') is None:
    raise Exception('docker is not installed.')
if which('docker-compose') is None:
    raise Exception('docker-compose is not installed.')

logging.config.dictConfig(logging_config.LOGGING)

# if __name__ == '__main__':

