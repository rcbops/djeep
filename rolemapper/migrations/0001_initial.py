# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Config'
        db.create_table('rolemapper_config', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolemapper.Cluster'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('rolemapper', ['Config'])

        # Adding model 'Cluster'
        db.create_table('rolemapper_cluster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('claim', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('rolemapper', ['Cluster'])

        # Adding model 'Host'
        db.create_table('rolemapper_host', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mac_address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('gateway', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('netmask', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('state', self.gf('django.db.models.fields.CharField')(default='unmanaged', max_length=255)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolemapper.Role'])),
            ('kick_target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolemapper.KickTarget'])),
            ('local_boot', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolemapper.Cluster'])),
            ('ipmi_ip', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('mgmt_ip', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('vmnet_ip', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
        ))
        db.send_create_signal('rolemapper', ['Host'])

        # Adding model 'KickTarget'
        db.create_table('rolemapper_kicktarget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('pxeconfig', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('kernel', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('initrd', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('preseed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('post_script', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('firstboot', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('rolemapper', ['KickTarget'])

        # Adding model 'Role'
        db.create_table('rolemapper_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('rolemapper', ['Role'])

        # Adding model 'RoleMap'
        db.create_table('rolemapper_rolemap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolemapper.Role'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('rolemapper', ['RoleMap'])


    def backwards(self, orm):
        
        # Deleting model 'Config'
        db.delete_table('rolemapper_config')

        # Deleting model 'Cluster'
        db.delete_table('rolemapper_cluster')

        # Deleting model 'Host'
        db.delete_table('rolemapper_host')

        # Deleting model 'KickTarget'
        db.delete_table('rolemapper_kicktarget')

        # Deleting model 'Role'
        db.delete_table('rolemapper_role')

        # Deleting model 'RoleMap'
        db.delete_table('rolemapper_rolemap')


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
        }
    }

    complete_apps = ['rolemapper']
