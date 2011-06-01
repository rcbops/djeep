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

@app.route('/chef_key', methods=['POST'])
# curl -H "Content-type: application/octet-stream" -XPOST --data-binary \
#     @key.file <url>
def post_chef_key():
    key = flask.request.data

    tv = models.TemplateVars.query.filter(models.TemplateVars.key == 'chef_key').first()
    if tv == None:
        tv = models.TemplateVars()
        tv.key = 'chef_key'
        tv.value = key
    else:
        tv.value = key

    rv = models.commit(tv)

    return 'add/update chef key\n'

@app.route('/chef_key', methods=['GET'])
def get_chef_key():
    tv = models.TemplateVars.query.filter(models.TemplateVars.key == 'chef_key').first()
    response = app.make_response('')

    if tv is None:
        response.status_code = 404
        response.data = "Error:  No chef key present\n"
    else:
        response.data = tv.value

    return response

