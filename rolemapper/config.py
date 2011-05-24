import os

# 127.0.0.1 to listen only on local interface
# 0.0.0.0 to listen on all interfaces
# any other ip to bind to a specific interface
HOST = '0.0.0.0'

# Turn this off in production, it allows user input code execution
DEBUG = True

# This is a good default for development
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/../webapp.db' % os.path.dirname(__file__)
