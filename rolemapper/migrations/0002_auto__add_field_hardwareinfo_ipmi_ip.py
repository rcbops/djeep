# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'HardwareInfo.ipmi_ip'
        db.add_column('rolemapper_hardwareinfo', 'ipmi_ip', self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'HardwareInfo.ipmi_ip'
        db.delete_column('rolemapper_hardwareinfo', 'ipmi_ip')


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
            'hardware_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'ipmi_ip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'kick_target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.KickTarget']"}),
            'mac_address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'netmask': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unmanaged'", 'max_length': '255'})
        },
        'rolemapper.kicktarget': {
            'Meta': {'object_name': 'KickTarget'},
            'firstboot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initrd': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'kernel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'post_script': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'preseed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
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
