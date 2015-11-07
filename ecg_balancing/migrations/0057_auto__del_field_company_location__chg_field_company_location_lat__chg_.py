# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Company.location'
        db.delete_column(u'ecg_balancing_company', 'location')


        # Changing field 'Company.location_lat'
        db.alter_column(u'ecg_balancing_company', 'location_lat', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6))

        # Changing field 'Company.location_lon'
        db.alter_column(u'ecg_balancing_company', 'location_lon', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6))

    def backwards(self, orm):
        # Adding field 'Company.location'
        db.add_column(u'ecg_balancing_company', 'location',
                      self.gf('osm_field.fields.OSMField')(null=True),
                      keep_default=False)


        # Changing field 'Company.location_lat'
        db.alter_column(u'ecg_balancing_company', u'location_lat', self.gf('osm_field.fields.LatitudeField')())

        # Changing field 'Company.location_lon'
        db.alter_column(u'ecg_balancing_company', u'location_lon', self.gf('osm_field.fields.LongitudeField')())

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
            'affiliates': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'foundation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'location_lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'managing_directors': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'model_creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owners': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "u'name'", 'unique_with': '()'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'not-approved'", 'max_length': '20'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visibility': ('django.db.models.fields.CharField', [], {'default': "u'basic'", 'max_length': '10'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zipcode': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'ecg_balancing.companybalance': {
            'Meta': {'object_name': 'CompanyBalance'},
            'accompanying_consultant': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'auditor': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'common_good': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'balance'", 'to': u"orm['ecg_balancing.Company']"}),
            'consultant': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'balances_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'employees_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'evaluation_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_communication': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'matrix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'company_balances'", 'to': u"orm['ecg_balancing.ECGMatrix']"}),
            'number_participated_employees': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'peer_companies': ('django.db.models.fields.related.ManyToManyField', [], {'max_length': '255', 'to': u"orm['ecg_balancing.Company']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'points': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'max_length': '4'}),
            'process_description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'profit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2'}),
            'prospect': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'revenue': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'balances_updated'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'visibility': ('django.db.models.fields.CharField', [], {'default': "u'internal'", 'max_length': '15'}),
            'worked_hours': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'})
        },
        u'ecg_balancing.companybalanceindicator': {
            'Meta': {'object_name': 'CompanyBalanceIndicator'},
            'company_balance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'company_balance'", 'to': u"orm['ecg_balancing.CompanyBalance']"}),
            'description': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'evaluation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'evaluation_table': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'company_balance'", 'to': u"orm['ecg_balancing.Indicator']"}),
            'key_figures': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'relevance': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'relevance_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ecg_balancing.ecgmatrix': {
            'Meta': {'object_name': 'ECGMatrix'},
            'contact': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "u'4.1'", 'max_length': '6'})
        },
        u'ecg_balancing.feedbackindicator': {
            'Meta': {'object_name': 'FeedbackIndicator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'feedback'", 'to': u"orm['ecg_balancing.Indicator']"}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'receiver_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'receiver_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'ecg_balancing.indicator': {
            'Meta': {'object_name': 'Indicator'},
            'contact': ('ecg_balancing.fields.CommaSeparatedEmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'ecg_value': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'evaluation_table': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_figures': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'matrix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'indicators'", 'to': u"orm['ecg_balancing.ECGMatrix']"}),
            'max_evaluation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'parent_indicator'", 'null': 'True', 'to': u"orm['ecg_balancing.Indicator']"}),
            'relevance': ('django.db.models.fields.CharField', [], {'default': "u'middle'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'sole_proprietorship': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stakeholder': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subindicator_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'ecg_balancing.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'ecg_balancing.userrole': {
            'Meta': {'object_name': 'UserRole'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ecg_balancing.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'role'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['ecg_balancing']