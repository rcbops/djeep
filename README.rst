BLEEP
=====

Welcome to a goldmine of OpenStack server management stuff.


Features
--------
 * Manage PXE configurations for multiple servers.
 * Preseed templates for assigning `puppet` roles.


Usage
-----

 * We use South for migrations, you'll probably do something like::

  python manage.py syncdb
  python manage.py migrate


TODO
----
 * Automatic hardware discovery. Wouldn't that be swell?
