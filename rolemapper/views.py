import flask

from rolemapper import app, db
from rolemapper import models


@app.route('/', methods=['GET'])
def hello():
    hw = models.HardwareInfo.query.all()
    return '<br/>'.join([x.mac_address for x in hw])


@app.route('/', methods=['POST'])
def create():
    req = flask.request
    hw = models.HardwareInfo()
    hw.mac_address = req.form['mac_address']
    hw.hardware_info = req.form['hardware_info']
    rv = models.commit(hw)
    return 'create: %r // %r' % (hw, rv)


@app.route('/form', methods=['GET'])
def form():
    return flask.render_template('form.html', postback=flask.url_for('create'))
