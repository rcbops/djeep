# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TemplateVar'
        db.create_table('rolemapper_templatevar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('rolemapper', ['TemplateVar'])

        # Adding model 'HardwareInfo'
        db.create_table('rolemapper_hardwareinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mac_address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('hardware_info', self.gf('django.db.models.fields.TextField')()),
            ('ip_address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('gateway', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('netmask', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('state', self.gf('django.db.models.fields.CharField')(default='unmanaged', max_length=255)),
            ('kick_target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolemapper.KickTarget'])),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolemapper.Cluster'])),
        ))
        db.send_create_signal('rolemapper', ['HardwareInfo'])

        # Adding model 'Cluster'
        db.create_table('rolemapper_cluster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('rolemapper', ['Cluster'])

        # Adding model 'KickTarget'
        db.create_table('rolemapper_kicktarget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('pxeconfig', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('kernel', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('initrd', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('preseed', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('post_script', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('firstboot', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('rolemapper', ['KickTarget'])


    def backwards(self, orm):
        
        # Deleting model 'TemplateVar'
        db.delete_table('rolemapper_templatevar')

        # Deleting model 'HardwareInfo'
        db.delete_table('rolemapper_hardwareinfo')

        # Deleting model 'Cluster'
        db.delete_table('rolemapper_cluster')

        # Deleting model 'KickTarget'
        db.delete_table('rolemapper_kicktarget')


    models = {
        'rolemapper.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'rolemapper.hardwareinfo': {
            'Meta': {'object_name': 'HardwareInfo'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.Cluster']"}),
            'gateway': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'hardware_info': ('django.db.models.fields.TextField', [], {}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'kick_target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.KickTarget']"}),
            'mac_address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'netmask': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unmanaged'", 'max_length': '255'})
        },
        'rolemapper.kicktarget': {
            'Meta': {'object_name': 'KickTarget'},
            'firstboot': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initrd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'kernel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'post_script': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'preseed': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pxeconfig': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'rolemapper.templatevar': {
            'Meta': {'object_name': 'TemplateVar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['rolemapper']
