import flask

from rolemapper import app, db
from rolemapper import models


@app.route('/', methods=['GET'])
def html_default():
    return flask.render_template('default.html')    

@app.route('/hardware', methods=['GET'])
def html_show_hardware():
    hw = models.HardwareInfo.query.all()
    return flask.render_template('show_hardware.html', hw=hw)

@app.route('/hardware', methods=['POST'])
def create():
    req = flask.request
    hw = models.HardwareInfo()
    hw.mac_address = req.form['mac_address']
    hw.hardware_info = req.form['hardware_info']
    rv = models.commit(hw)
    return 'create: %r // %r' % (hw, rv)

@app.route('/form', methods=['GET'])
def form():
    return flask.render_template('form.html',
                                 postback=flask.url_for('create'))

@app.route('/chef_key', methods=['POST'])
# curl -H "Content-type: application/octet-stream" -XPOST --data-binary \
#     @key.file http://<server>:<port>/chef_key
def post_chef_key():
    key = flask.request.data

    tv = models.TemplateVars.query.filter(
            models.TemplateVars.key == 'chef_key').first()

    if tv == None:
        tv = models.TemplateVars()
        tv.key = 'chef_key'
        tv.value = key
    else:
        tv.value = key

    rv = models.commit(tv)

    return 'add/update chef key\n'

@app.route('/chef_key', methods=['GET'])
# curl -skS -o validation.pem http://<server>:<port>/chef_key
def get_chef_key():
    tv = models.TemplateVars.query.filter(
            models.TemplateVars.key == 'chef_key').first_or_404()

    response.data = tv.value
    return response

@app.route('/preseed/<host_id>', methods=['GET'])
def generate_preseed(host_id):
    # we should pull dist and arch from the host info, as
    # we needed it to write out the pxelinux.cfg template
    #
    # hardware info should really be host info
    hw = models.HardwareInfo.query.get_or_404(host_id)
    
    host_dist = 'maverick'
    host_arch = 'amd64'

    kvpairs = models.TemplateVars.query.all()
    site = dict(zip([x.key for x in kvpairs], [x.value for x in kvpairs]))

    template_file = 'preseed/%s-%s-preseed.txt' % (host_dist, host_arch)
    return flask.render_template(template_file, host=hw, site=site)
    
# Key/value pair management (web based)
@app.route('/keys/', methods=['GET'])
def html_show_keys():
    kvpairs = models.TemplateVars.query.all()
    site = dict(zip([x.key for x in kvpairs], [x.value for x in kvpairs]))
    return flask.render_template('show_keys.html', site=site)

@app.route('/keys/delete/<key>', methods=['GET'])
def html_delete_key(key):
    tv = models.TemplateVars.query.filter(
            models.TemplateVars.key == key).first_or_404()

    db.session.delete(tv)
    db.session.commit()

    flask.flash('deleted')
    return flask.redirect(flask.url_for('html_show_keys'));

@app.route('/keys/edit/<key>', methods=['GET'])
def html_edit_key(key):
    tv = models.TemplateVars.query.filter(
            models.TemplateVars.key == key).first_or_404()
    return flask.render_template('html_edit_key.html', input = { 'key': tv.key,
                                                                 'value': tv.value })
    
@app.route('/keys/edit/<key>', methods=['POST'])
def html_post_edit_key(key):
    req = flask.request
    tv = models.TemplateVars.query.filter(
            models.TemplateVars.key == req.form['key']).first()

    action = 'Edited'
    if tv == None:
        tv = models.TemplateVars()
        tv.key = req.form['key']
        tv.value = req.form['value']
        action = 'Created'
    else:
        tv.value = req.form['value']

    rv = models.commit(tv)
    flask.flash('%s key' % (action, ))
    return flask.redirect(flask.url_for('html_show_keys'));
    
@app.route('/keys/add/', methods=['GET'])
def html_add_key():
    return flask.render_template('html_edit_key.html', input = { 'key': '',
                                                                 'value': '' })

@app.route('/keys/add/', methods=['POST'])
def html_post_add_key():
    return html_post_edit_key(None)

