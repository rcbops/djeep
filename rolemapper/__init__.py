import flask
from flaskext import sqlalchemy

app = flask.Flask(__name__)
app.config.from_object('rolemapper.config')
app.secret_key = "supersecretsecretkey"
session_options={"autocommit": True}
db = sqlalchemy.SQLAlchemy(app,session_options=session_options)
