from os import path
import sys
import logging
sys.path.insert(0, path.dirname(path.realpath(__file__)))  # parent dir
sys.path.insert(0, path.join(path.dirname(path.realpath(__file__)), "vocprez"))  # vocprez dir
logging.basicConfig(stream=sys.stderr)

from app import app as application
