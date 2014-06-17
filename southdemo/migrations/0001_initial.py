# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lizard'
        db.create_table(u'southdemo_lizard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'southdemo', ['Lizard'])

        # Adding model 'Adopter'
        db.create_table(u'southdemo_adopter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lizard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['southdemo.Lizard'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'southdemo', ['Adopter'])


    def backwards(self, orm):
        # Deleting model 'Lizard'
        db.delete_table(u'southdemo_lizard')

        # Deleting model 'Adopter'
        db.delete_table(u'southdemo_adopter')


    models = {
        u'southdemo.adopter': {
            'Meta': {'object_name': 'Adopter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lizard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['southdemo.Lizard']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'southdemo.lizard': {
            'Meta': {'object_name': 'Lizard'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['southdemo']