'''
mod_wsgi script for running the MultiScanner web app with Apache
'''

import sys

sys.path.insert(0, '/opt/multiscanner/web')

from app import app as application

