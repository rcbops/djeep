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
  python manage.py runeventlet 8080


That will ask you to make an admin user, you'll use that to get into the admin.

We'll want to add some fixtures: https://docs.djangoproject.com/en/1.3/howto/initial-data/

To mess with how the data is displayed in the admin: https://docs.djangoproject.com/en/1.3/ref/contrib/admin/


Updating
--------

 1. Make a backup::

    $ python manage.py dumpdata --format=yaml rolemapper > backup.yaml

 2. Update the code::

    $ git pull origin master

 3. Reset everything for good measure::

    $ ./reset.sh

 4. Load your data::

    $ python manage.py loaddata backup.yaml


Actions Somebody Might Want To Do With A Cluster
------------------------------------------------

 * (DONE) Re-deploy
 * (DONE) Claim/Lock so that other people do not re-deploy
 * (DONE) Free to tell others it is free to use
 * Notifications of beginning / end of redeploy
 * Generate munin config files, specifically the per-cluster list of nodes.
 * Manage a puppet server per-cluster

Actions Somebody Might Want To Do With A Host
---------------------------------------------

 * (DONE) Reboot
 * (DONE) Re-assign to a new cluster
 * Notifications when reboot complete
 * Per-host overrides of key-value pairs

General Hoped For Functionality
-------------------------------

 * Template-ability of values.
   * Would be nice to express something like "the api endpoint is the ip of
     the machine with the nova-infra role"... something like: api_endpoint={{ roles[nova-infra][0].ip }} ... ish
 * (DONE) More optimized updates, for batch updates don't rekick and rewrite
   until they've all been updated.
 * Configure global and cluster configs separately.

TODO
----
 * Automatic hardware discovery. Wouldn't that be swell?
