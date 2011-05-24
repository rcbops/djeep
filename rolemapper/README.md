This is the source directory containg the webapp that collects hardware
information and lets users tag machines with chef roles.

# Installation

Create virtualenv, install database, configure.

```shell
cd ..
python ./tools/install_venv.py
./tools/with_venv.sh python rolemapper/syncdb.py
vi rolemapper/config.py
```

# Running (development)

Start the server.

```shell
cd ..
./tools/with_venv.sh python server.py
```

# Running (production)

TODO (todd): make this all work
Turn off debugging in config.py
Run under apache mod_wsgi, see http://flask.pocoo.org/docs/deploying/mod_wsgi/
