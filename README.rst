DJEEP
=====

Welcome to a goldmine of OpenStack server management stuff.


Features
--------
 * Manage PXE configurations for multiple servers.
 * Preseed templates for assigning `puppet` roles.


Usage
-----

We use South for migrations, you'll probably do something like::

  python manage.py syncdb
  python manage.py migrate
  python manage.py runserver 8080


That will ask you to make an admin user, you'll use that to get into the admin.

We'll want to add some fixtures: https://docs.djangoproject.com/en/1.3/howto/initial-data/

To mess with how the data is displayed in the admin: https://docs.djangoproject.com/en/1.3/ref/contrib/admin/


Actions Somebody Might Want To Do With A Cluster
------------------------------------------------

 * Re-deploy
 * Claim/Lock so that other people do not re-deploy
 * Free to tell others it is free to use
 * Notifications of beginning / end of redeploy


Actions Somebody Might Want To Do With A Host
---------------------------------------------

 * Reboot
 * Re-assign to a new cluster
 * Notifications when reboot complete



TODO
----
 * Automatic hardware discovery. Wouldn't that be swell?
