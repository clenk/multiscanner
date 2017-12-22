'''
mod_wsgi script for running the MultiScanner REST app with Apache
'''

import sys

sys.path.insert(0, '/opt/multiscanner/utils')

from api import app as application
