#!/usr/bin/env python
from migrate.versioning.shell import main
main(url='sqlite:///../webapp.db', debug='False', repository='migration/')
