# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'ecg_balancing_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name=u'profile', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'ecg_balancing', ['UserProfile'])

        # Adding M2M table for field companies on 'UserProfile'
        m2m_table_name = db.shorten_name(u'ecg_balancing_userprofile_companies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'ecg_balancing.userprofile'], null=False)),
            ('company', models.ForeignKey(orm[u'ecg_balancing.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'company_id'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'ecg_balancing_userprofile')

        # Removing M2M table for field companies on 'UserProfile'
        db.delete_table(db.shorten_name(u'ecg_balancing_userprofile_companies'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ecg_balancing.company': {
            'Meta': {'object_name': 'Company'},
            'activities': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'employees_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'foundation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'managing_directors': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'model_creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owners': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'revenue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zipcode': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'ecg_balancing.companybalance': {
            'Meta': {'object_name': 'CompanyBalance'},
            'auditor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'common_good': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'balance'", 'to': u"orm['ecg_balancing.Company']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matrix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'company_balances'", 'to': u"orm['ecg_balancing.ECGMatrix']"}),
            'peer_companies': ('django.db.models.fields.related.ManyToManyField', [], {'max_length': '255', 'to': u"orm['ecg_balancing.Company']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'process_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'prospect': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ecg_balancing.companybalanceindicator': {
            'Meta': {'object_name': 'CompanyBalanceIndicator'},
            'company_balance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'company_balance'", 'to': u"orm['ecg_balancing.CompanyBalance']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'evaluation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'company_balance'", 'to': u"orm['ecg_balancing.Indicator']"})
        },
        u'ecg_balancing.ecgmatrix': {
            'Meta': {'object_name': 'ECGMatrix'},
            'contact': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "u'4.1'", 'max_length': '6'})
        },
        u'ecg_balancing.indicator': {
            'Meta': {'object_name': 'Indicator'},
            'contact': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'ecg_value': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matrix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'indicators'", 'to': u"orm['ecg_balancing.ECGMatrix']"}),
            'max_evaluation': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'parent_indicator'", 'null': 'True', 'to': u"orm['ecg_balancing.Indicator']"}),
            'stakeholder': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subindicator_number': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'ecg_balancing.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'companies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['ecg_balancing.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'ecg_balancing.userrole': {
            'Meta': {'object_name': 'UserRole'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ecg_balancing.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['ecg_balancing']