# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AppUser'
        db.delete_table(u'motsdits_appuser')

        # Removing M2M table for field user_permissions on 'AppUser'
        db.delete_table(db.shorten_name(u'motsdits_appuser_user_permissions'))

        # Removing M2M table for field guides on 'AppUser'
        db.delete_table(db.shorten_name(u'motsdits_appuser_guides'))

        # Removing M2M table for field groups on 'AppUser'
        db.delete_table(db.shorten_name(u'motsdits_appuser_groups'))

        # Adding model 'User'
        db.create_table(u'motsdits_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('primary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.UserGuide'], null=True)),
            ('profile_photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('lng', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'motsdits', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'motsdits_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'motsdits.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'motsdits_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'motsdits.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding M2M table for field guides on 'User'
        m2m_table_name = db.shorten_name(u'motsdits_user_guides')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'motsdits.user'], null=False)),
            ('userguide', models.ForeignKey(orm[u'motsdits.userguide'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'userguide_id'])


        # Changing field 'MotDit.created_by'
        db.alter_column(u'motsdits_motdit', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.User'], null=True))

        # Changing field 'UserGuide.created_by'
        db.alter_column(u'motsdits_userguide', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.User'], null=True))

        # Changing field 'Category.created_by'
        db.alter_column(u'motsdits_category', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.User'], null=True))

        # Changing field 'Activity.created_by'
        db.alter_column(u'motsdits_activity', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.User'], null=True))

        # Changing field 'Tag.created_by'
        db.alter_column(u'motsdits_tag', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.User'], null=True))

        # Changing field 'Opinion.created_by'
        db.alter_column(u'motsdits_opinion', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.User'], null=True))

        # Changing field 'Subfilter.created_by'
        db.alter_column(u'motsdits_subfilter', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.User'], null=True))

        # Changing field 'Photo.created_by'
        db.alter_column(u'motsdits_photo', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.User'], null=True))

    def backwards(self, orm):
        # Adding model 'AppUser'
        db.create_table(u'motsdits_appuser', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('primary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.UserGuide'], null=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lng', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('profile_photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'motsdits', ['AppUser'])

        # Adding M2M table for field user_permissions on 'AppUser'
        m2m_table_name = db.shorten_name(u'motsdits_appuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('appuser', models.ForeignKey(orm[u'motsdits.appuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['appuser_id', 'permission_id'])

        # Adding M2M table for field guides on 'AppUser'
        m2m_table_name = db.shorten_name(u'motsdits_appuser_guides')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('appuser', models.ForeignKey(orm[u'motsdits.appuser'], null=False)),
            ('userguide', models.ForeignKey(orm[u'motsdits.userguide'], null=False))
        ))
        db.create_unique(m2m_table_name, ['appuser_id', 'userguide_id'])

        # Adding M2M table for field groups on 'AppUser'
        m2m_table_name = db.shorten_name(u'motsdits_appuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('appuser', models.ForeignKey(orm[u'motsdits.appuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['appuser_id', 'group_id'])

        # Deleting model 'User'
        db.delete_table(u'motsdits_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'motsdits_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'motsdits_user_user_permissions'))

        # Removing M2M table for field guides on 'User'
        db.delete_table(db.shorten_name(u'motsdits_user_guides'))


        # Changing field 'MotDit.created_by'
        db.alter_column(u'motsdits_motdit', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.AppUser'], null=True))

        # Changing field 'UserGuide.created_by'
        db.alter_column(u'motsdits_userguide', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.AppUser'], null=True))

        # Changing field 'Category.created_by'
        db.alter_column(u'motsdits_category', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.AppUser'], null=True))

        # Changing field 'Activity.created_by'
        db.alter_column(u'motsdits_activity', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.AppUser'], null=True))

        # Changing field 'Tag.created_by'
        db.alter_column(u'motsdits_tag', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.AppUser'], null=True))

        # Changing field 'Opinion.created_by'
        db.alter_column(u'motsdits_opinion', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.AppUser'], null=True))

        # Changing field 'Subfilter.created_by'
        db.alter_column(u'motsdits_subfilter', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.AppUser'], null=True))

        # Changing field 'Photo.created_by'
        db.alter_column(u'motsdits_photo', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.AppUser'], null=True))

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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'motsdits.activity': {
            'Meta': {'object_name': 'Activity'},
            'activity_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'motsdits.category': {
            'Meta': {'object_name': 'Category'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        u'motsdits.motdit': {
            'Meta': {'object_name': 'MotDit'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'motdit'", 'null': 'True', 'to': u"orm['motsdits.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'recommendations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'motdit_recommendation'", 'symmetrical': 'False', 'to': u"orm['motsdits.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'null': 'True'}),
            'subfilters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'motdit'", 'symmetrical': 'False', 'to': u"orm['motsdits.Subfilter']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'motsdits'", 'symmetrical': 'False', 'to': u"orm['motsdits.Tag']"}),
            'top_opinion': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'motdit_top'", 'null': 'True', 'to': u"orm['motsdits.Opinion']"}),
            'top_photo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'motdit_top'", 'null': 'True', 'to': u"orm['motsdits.Photo']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'motsdits.opinion': {
            'Meta': {'object_name': 'Opinion'},
            'approvals': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'approvals'", 'symmetrical': 'False', 'to': u"orm['motsdits.User']"}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.User']", 'null': 'True'}),
            'dislikes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'dislikes'", 'symmetrical': 'False', 'to': u"orm['motsdits.User']"}),
            'format': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motdit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opinions'", 'to': u"orm['motsdits.MotDit']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'motsdits.photo': {
            'Meta': {'object_name': 'Photo'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'photo_likes'", 'symmetrical': 'False', 'to': u"orm['motsdits.User']"}),
            'motdit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['motsdits.MotDit']"}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'motsdits.subfilter': {
            'Meta': {'object_name': 'Subfilter'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'}),
            'subfilter_type': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'motsdits.tag': {
            'Meta': {'object_name': 'Tag'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'motsdits.user': {
            'Meta': {'object_name': 'User'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'guides': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'guides'", 'symmetrical': 'False', 'to': u"orm['motsdits.UserGuide']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.UserGuide']", 'null': 'True'}),
            'profile_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'motsdits.userguide': {
            'Meta': {'object_name': 'UserGuide'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motsdits': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'motsdits'", 'symmetrical': 'False', 'to': u"orm['motsdits.MotDit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['motsdits']