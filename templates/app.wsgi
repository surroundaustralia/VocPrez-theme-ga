import sys
import logging
sys.path.insert(0, '/var/www/ga')
sys.path.insert(0, '/var/www/ga/vocprez')
logging.basicConfig(stream=sys.stderr)

from app import app as application
