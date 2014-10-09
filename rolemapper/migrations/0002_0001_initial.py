# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SSHKey'
        db.create_table('rolemapper_sshkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('private_key', self.gf('django.db.models.fields.TextField')()),
            ('public_key', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('rolemapper', ['SSHKey'])

        # Adding field 'Host.ssh_key'
        db.add_column('rolemapper_host', 'ssh_key',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolemapper.SSHKey'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'SSHKey'
        db.delete_table('rolemapper_sshkey')

        # Deleting field 'Host.ssh_key'
        db.delete_column('rolemapper_host', 'ssh_key_id')


    models = {
        'rolemapper.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'claim': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'rolemapper.config': {
            'Meta': {'object_name': 'Config'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.Cluster']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'rolemapper.host': {
            'Meta': {'object_name': 'Host'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.Cluster']"}),
            'gateway': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'ipmi_ip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'kick_target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.KickTarget']"}),
            'local_boot': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'mgmt_ip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'netmask': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.Role']"}),
            'ssh_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.SSHKey']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unmanaged'", 'max_length': '255'}),
            'vmnet_ip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
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
        'rolemapper.role': {
            'Meta': {'object_name': 'Role'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'rolemapper.rolemap': {
            'Meta': {'object_name': 'RoleMap'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolemapper.Role']"})
        },
        'rolemapper.sshkey': {
            'Meta': {'object_name': 'SSHKey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'private_key': ('django.db.models.fields.TextField', [], {}),
            'public_key': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['rolemapper']