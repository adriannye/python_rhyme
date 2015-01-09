# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PartOfSpeech',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Parts of Speech',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PeerReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_added', models.BooleanField(default=False)),
                ('flagged', models.BooleanField(default=False)),
                ('reviewed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhonemeSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255, db_index=True)),
            ],
            options={
                'ordering': ['text'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RhymePhonemeSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sound', models.CharField(max_length=30)),
                ('rhyme_type', models.CharField(max_length=20, choices=[(b'FAMILY', b'Family'), (b'ADDITIVE', b'Additive'), (b'SUBTRACTIVE', b'Subtractive')])),
                ('order', models.IntegerField()),
                ('original_ps', models.ForeignKey(related_name='original_phoneme_sequences', to='rhyme.PhonemeSequence')),
                ('rhyme_ps', models.ForeignKey(related_name='rhyme_phoneme_sequences', to='rhyme.PhonemeSequence')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(unique=True, max_length=255, db_index=True)),
                ('parts_of_speech', models.ManyToManyField(to='rhyme.PartOfSpeech')),
                ('phoneme_sequence', models.ForeignKey(to='rhyme.PhonemeSequence')),
            ],
            options={
                'ordering': ['word'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='peerreview',
            name='word',
            field=models.OneToOneField(to='rhyme.Word'),
            preserve_default=True,
        ),
    ]
