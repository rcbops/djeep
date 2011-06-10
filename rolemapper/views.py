import flask

from rolemapper import app, db
from rolemapper import models
from formalchemy import FieldSet
from jinja2 import TemplateNotFound

@app.route('/', methods=['GET'])
def html_default():
    return flask.render_template('default.html', models=models.ModelList)

@app.route('/admin/<obj>/view', methods=['GET'])
def html_object_grid(obj):
    if not obj in models.ModelList.keys():
        flask.abort(404)

    obj_class = models.ModelList[obj]

    info = {}
    info['field_names'] = obj_class.__table__.columns.keys()
    info['key'] = obj_class.__table__.primary_key.columns.keys()[0]
    info['objects'] = obj_class.query.all()
    info['obj']  = obj

    template = 'table_view.html'
    if flask.request.accept_mimetypes.best_match(['application/json','text/html']) == \
            'application/json':
            
        output = { 'hardware': [] }
        for response_object in info['objects']:
            out_obj = {}
            for field in info['field_names']:
                out_obj[field] = getattr(response_object,field)
            output['hardware'].append(out_obj)
        return flask.jsonify(output)

    return flask.render_template(template, info=info)

@app.route('/admin/<obj>/new', methods=['GET', 'POST'])
def html_object_new(obj):
    return html_object_edit(obj, None)

@app.route('/admin/<obj>/delete/<key>', methods=['GET'])
def html_object_delete(obj, key):
    if not obj in models.ModelList.keys():
        flask.abort(404)

    obj_class = models.ModelList[obj]
    o = obj_class.query.get_or_404(key)

    db.session.delete(o)
    db.session.flush()
    
    return flask.redirect(flask.url_for('html_object_grid',
                                        obj = obj))

@app.route('/admin/<obj>/edit/<key>', methods=['GET', 'POST'])
def html_object_edit(obj, key):
    if not obj in models.ModelList.keys():
        flask.abort(404)

    obj_class = models.ModelList[obj]
    info = {}

    info['field_names'] = obj_class.__table__.columns.keys()
    info['key'] = obj_class.__table__.primary_key.columns.keys()[0]
    info['obj']  = obj

    if key and obj_class.query.get(key):
        info['object'] = obj_class.query.get(key)
        info['fields'] = FieldSet(info['object'])
    else:
        info['object'] = obj_class()
        info['fields'] = FieldSet(obj_class, session=db.session)

    retval = ""
    if flask.request.method == 'POST':
        # This is the postback
        if flask.request.content_type == 'application/json':
            payload = flask.request.json

            for key in payload.keys():
                info['object'].__setattr__(key, payload[key])

        else:
            callback_info = dict(flask.request.form.items())
            fields = FieldSet(info['object'], data = callback_info)
            
            if fields.validate():
                fields.sync()

            retval = flask.redirect(flask.url_for('html_object_grid',
                                                  obj = obj))
        models.commit(info['object'])
        return retval
    
    info['form_data'] = info['fields'].render()
    return flask.render_template('table_edit.html', info=info)

# we can get rid of this, I think
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

@app.route('/template/<template_type>/<host_id>', methods=['GET'])
def generate_template(template_type, host_id):
    if template_type not in ['preseed', 'post_script']:
        flask.abort(404)
        
    hw = models.HardwareInfo.query.get_or_404(host_id)
    kvpairs = models.TemplateVars.query.all()
    site = dict(zip([x.key for x in kvpairs], [x.value for x in kvpairs]))

    # the template type is one of:
    #  * preseed
    #  * post_script

    template_file = hw.kick_target.__getattribute__(template_type)

    try:
        return flask.render_template(template_file, host=hw, site=site)
    except TemplateNotFound:
        flask.abort(404)
        

