#!/usr/bin/python3

import logging
import sys

logging.basicConfig(stream=sys.stderr)

from app import app as application
application.secret = "kesako"