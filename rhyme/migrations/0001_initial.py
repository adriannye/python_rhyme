# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PeerReview'
        db.create_table(u'rhyme_peerreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_added', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flagged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reviewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('added_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'rhyme', ['PeerReview'])

        # Adding model 'PhonemeSequence'
        db.create_table(u'rhyme_phonemesequence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'rhyme', ['PhonemeSequence'])

        # Adding model 'RhymePhonemeSequence'
        db.create_table(u'rhyme_rhymephonemesequence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sound', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('original_ps', self.gf('django.db.models.fields.related.ForeignKey')(related_name='original_phoneme_sequences', to=orm['rhyme.PhonemeSequence'])),
            ('rhyme_ps', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rhyme_phoneme_sequences', to=orm['rhyme.PhonemeSequence'])),
            ('rhyme_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'rhyme', ['RhymePhonemeSequence'])

        # Adding model 'PartOfSpeech'
        db.create_table(u'rhyme_partofspeech', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'rhyme', ['PartOfSpeech'])

        # Adding model 'Word'
        db.create_table(u'rhyme_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('phoneme_sequence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rhyme.PhonemeSequence'])),
            ('peer_review', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['rhyme.PeerReview'], unique=True)),
        ))
        db.send_create_signal(u'rhyme', ['Word'])

        # Adding M2M table for field parts_of_speech on 'Word'
        m2m_table_name = db.shorten_name(u'rhyme_word_parts_of_speech')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('word', models.ForeignKey(orm[u'rhyme.word'], null=False)),
            ('partofspeech', models.ForeignKey(orm[u'rhyme.partofspeech'], null=False))
        ))
        db.create_unique(m2m_table_name, ['word_id', 'partofspeech_id'])


    def backwards(self, orm):
        # Deleting model 'PeerReview'
        db.delete_table(u'rhyme_peerreview')

        # Deleting model 'PhonemeSequence'
        db.delete_table(u'rhyme_phonemesequence')

        # Deleting model 'RhymePhonemeSequence'
        db.delete_table(u'rhyme_rhymephonemesequence')

        # Deleting model 'PartOfSpeech'
        db.delete_table(u'rhyme_partofspeech')

        # Deleting model 'Word'
        db.delete_table(u'rhyme_word')

        # Removing M2M table for field parts_of_speech on 'Word'
        db.delete_table(db.shorten_name(u'rhyme_word_parts_of_speech'))


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'rhyme.partofspeech': {
            'Meta': {'object_name': 'PartOfSpeech'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'rhyme.peerreview': {
            'Meta': {'object_name': 'PeerReview'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'added_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_added': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'rhyme.phonemesequence': {
            'Meta': {'object_name': 'PhonemeSequence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'rhyme.rhymephonemesequence': {
            'Meta': {'object_name': 'RhymePhonemeSequence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'original_ps': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'original_phoneme_sequences'", 'to': u"orm['rhyme.PhonemeSequence']"}),
            'rhyme_ps': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rhyme_phoneme_sequences'", 'to': u"orm['rhyme.PhonemeSequence']"}),
            'rhyme_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sound': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'rhyme.word': {
            'Meta': {'object_name': 'Word'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parts_of_speech': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['rhyme.PartOfSpeech']", 'symmetrical': 'False'}),
            'peer_review': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['rhyme.PeerReview']", 'unique': 'True'}),
            'phoneme_sequence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rhyme.PhonemeSequence']"}),
            'word': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['rhyme']