# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'motsdits_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'motsdits', ['Category'])

        # Adding model 'MotDit'
        db.create_table(u'motsdits_motdit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mot', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'motsdits', ['MotDit'])

        # Adding M2M table for field category on 'MotDit'
        m2m_table_name = db.shorten_name(u'motsdits_motdit_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('motdit', models.ForeignKey(orm[u'motsdits.motdit'], null=False)),
            ('category', models.ForeignKey(orm[u'motsdits.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['motdit_id', 'category_id'])

        # Adding M2M table for field recommendations on 'MotDit'
        m2m_table_name = db.shorten_name(u'motsdits_motdit_recommendations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('motdit', models.ForeignKey(orm[u'motsdits.motdit'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['motdit_id', 'user_id'])

        # Adding model 'Avis'
        db.create_table(u'motsdits_avis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('motdit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='motdit', to=orm['motsdits.MotDit'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'motsdits', ['Avis'])

        # Adding M2M table for field approvals on 'Avis'
        m2m_table_name = db.shorten_name(u'motsdits_avis_approvals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('avis', models.ForeignKey(orm[u'motsdits.avis'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['avis_id', 'user_id'])

        # Adding model 'Photo'
        db.create_table(u'motsdits_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('motdit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['motsdits.MotDit'], unique=True)),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'motsdits', ['Photo'])

        # Adding M2M table for field likes on 'Photo'
        m2m_table_name = db.shorten_name(u'motsdits_photo_likes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm[u'motsdits.photo'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photo_id', 'user_id'])

        # Adding model 'UserGuide'
        db.create_table(u'motsdits_userguide', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'motsdits', ['UserGuide'])

        # Adding M2M table for field motsdits on 'UserGuide'
        m2m_table_name = db.shorten_name(u'motsdits_userguide_motsdits')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userguide', models.ForeignKey(orm[u'motsdits.userguide'], null=False)),
            ('motdit', models.ForeignKey(orm[u'motsdits.motdit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userguide_id', 'motdit_id'])

        # Adding model 'UserProfile'
        db.create_table(u'motsdits_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.UserGuide'])),
        ))
        db.send_create_signal(u'motsdits', ['UserProfile'])

        # Adding M2M table for field guides on 'UserProfile'
        m2m_table_name = db.shorten_name(u'motsdits_userprofile_guides')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'motsdits.userprofile'], null=False)),
            ('userguide', models.ForeignKey(orm[u'motsdits.userguide'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'userguide_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'motsdits_category')

        # Deleting model 'MotDit'
        db.delete_table(u'motsdits_motdit')

        # Removing M2M table for field category on 'MotDit'
        db.delete_table(db.shorten_name(u'motsdits_motdit_category'))

        # Removing M2M table for field recommendations on 'MotDit'
        db.delete_table(db.shorten_name(u'motsdits_motdit_recommendations'))

        # Deleting model 'Avis'
        db.delete_table(u'motsdits_avis')

        # Removing M2M table for field approvals on 'Avis'
        db.delete_table(db.shorten_name(u'motsdits_avis_approvals'))

        # Deleting model 'Photo'
        db.delete_table(u'motsdits_photo')

        # Removing M2M table for field likes on 'Photo'
        db.delete_table(db.shorten_name(u'motsdits_photo_likes'))

        # Deleting model 'UserGuide'
        db.delete_table(u'motsdits_userguide')

        # Removing M2M table for field motsdits on 'UserGuide'
        db.delete_table(db.shorten_name(u'motsdits_userguide_motsdits'))

        # Deleting model 'UserProfile'
        db.delete_table(u'motsdits_userprofile')

        # Removing M2M table for field guides on 'UserProfile'
        db.delete_table(db.shorten_name(u'motsdits_userprofile_guides'))


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
        u'motsdits.avis': {
            'Meta': {'object_name': 'Avis'},
            'approvals': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'approvals'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motdit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'motdit'", 'to': u"orm['motsdits.MotDit']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'motsdits.category': {
            'Meta': {'object_name': 'Category'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'motsdits.motdit': {
            'Meta': {'object_name': 'MotDit'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories'", 'symmetrical': 'False', 'to': u"orm['motsdits.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mot': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'recommendations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recommendations'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'motsdits.photo': {
            'Meta': {'object_name': 'Photo'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'likes'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'motdit': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['motsdits.MotDit']", 'unique': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'motsdits.userguide': {
            'Meta': {'object_name': 'UserGuide'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motsdits': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'motsdits'", 'symmetrical': 'False', 'to': u"orm['motsdits.MotDit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'motsdits.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'guides': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'guides'", 'symmetrical': 'False', 'to': u"orm['motsdits.UserGuide']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.UserGuide']"})
        }
    }

    complete_apps = ['motsdits']