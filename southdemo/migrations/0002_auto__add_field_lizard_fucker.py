# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lizard.fucker'
        db.add_column(u'southdemo_lizard', 'fucker',
                      self.gf('django.db.models.fields.CharField')(default='Bobby', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Lizard.fucker'
        db.delete_column(u'southdemo_lizard', 'fucker')


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
            'fucker': ('django.db.models.fields.CharField', [], {'default': "'Bobby'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['southdemo']